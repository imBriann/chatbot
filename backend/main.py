from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
import uuid
import datetime

from database import get_db, engine, Base
from models import Message, Conversation, Knowledge, Training
from rag_agent import consultar_agente
from training_pipeline import start_training

# Initialize Database
Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Asistente Unipamplona")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    sessionId: str
    message: str
    category: Optional[str] = None

class ChatResponse(BaseModel):
    id: str
    response: str
    category: str
    confidence: float
    relatedTopics: List[str]
    timestamp: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.post("/api/auth/login")
def login(req: LoginRequest):
    # Dummy login for testing
    if req.email == "admin@unipamplona.edu.co" and req.password == "admin123":
        return {"token": "fake-jwt-token"}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@app.post("/api/chat/message", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # 1. Recuperar o crear conversación
        conv = db.query(Conversation).filter(Conversation.id == request.sessionId).first()
        if not conv:
            conv = Conversation(id=request.sessionId, title="Nueva Conversación")
            db.add(conv)
            db.commit()
        
        # 2. Guardar mensaje del usuario
        user_msg = Message(
            conversation_id=conv.id,
            sender="user",
            text=request.message
        )
        db.add(user_msg)
        db.commit()
        
        # 3. Consultar al agente RAG con manejo de errores
        try:
            resultado = consultar_agente(request.message)
            respuesta_texto = resultado.get("result", "Lo siento, tuve un problema al procesar tu solicitud.")
            docs = resultado.get("source_documents", [])
            fuentes_relacionadas = ["Guía de Orientación Académica"] if docs else []
            confidence = 0.9 if docs else 0.5
        except Exception as e:
            print(f"Error en consultar_agente: {str(e)}")
            respuesta_texto = "Lo siento, tuve un problema al procesar tu solicitud. Por favor intenta de nuevo más tarde."
            docs = []
            fuentes_relacionadas = []
            confidence = 0.0
        
        # 4. Guardar respuesta del bot
        bot_msg = Message(
            conversation_id=conv.id,
            sender="bot",
            text=respuesta_texto,
            confidence=confidence,
            related_docs=[doc.page_content[:100] for doc in docs] if docs else []
        )
        db.add(bot_msg)
        conv.last_updated = datetime.datetime.utcnow()
        db.commit()
        
        return ChatResponse(
            id=str(bot_msg.id),
            response=respuesta_texto,
            category=request.category or "general",
            confidence=confidence,
            relatedTopics=fuentes_relacionadas,
            timestamp=datetime.datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        print(f"Error en chat_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail="Error al procesar la solicitud")

@app.get("/api/chat/history/{sessionId}")
def get_history(sessionId: str, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.conversation_id == sessionId).order_by(Message.timestamp).all()
    history = []
    for m in messages:
        history.append({
            "id": str(m.id),
            "text": m.text,
            "sender": m.sender,
            "timestamp": m.timestamp.isoformat() + "Z"
        })
    return {"messages": history}

@app.delete("/api/chat/history/{sessionId}")
def clear_history(sessionId: str, db: Session = Depends(get_db)):
    db.query(Message).filter(Message.conversation_id == sessionId).delete()
    db.commit()
    return {"status": "ok"}

@app.get("/api/categories")
def get_categories(db: Session = Depends(get_db)):
    # Retorna categorías estáticas por ahora o desde BD
    return {"categories": [
        {"id": "1", "name": "Inscripciones", "slug": "inscripciones", "description": "Proceso de admisión", "icon": "📝"},
        {"id": "2", "name": "Grados", "slug": "grados", "description": "Requisitos de grado", "icon": "🎓"},
    ]}

@app.get("/api/categories/{slug}/faqs")
def get_faqs_by_category(slug: str, db: Session = Depends(get_db)):
    faqs = db.query(Knowledge).filter(Knowledge.category.ilike(f"%{slug}%")).all()
    return {"faqs": [
        {"id": str(f.id), "question": f.question, "answer": f.answer, "categoryId": str(f.category)} 
        for f in faqs
    ]}

@app.get("/api/admin/metrics")
def get_metrics(db: Session = Depends(get_db)):
    # Fake metrics for now
    total_convs = db.query(Conversation).count()
    return {"metrics": {
        "totalConversations": total_convs,
        "activeUsers": 5,
        "successRate": 92.5,
        "avgResponseTime": 1.2
    }}

@app.get("/api/admin/logs")
def get_logs(limit: int = 20, db: Session = Depends(get_db)):
    messages = db.query(Message).filter(Message.sender == "user").order_by(Message.timestamp.desc()).limit(limit).all()
    return {"logs": [
        {
            "id": str(m.id),
            "timestamp": m.timestamp.isoformat() + "Z",
            "type": "info",
            "message": f"User asked: {m.text}",
            "details": f"Conversation {m.conversation_id}"
        } for m in messages
    ]}

@app.get("/api/admin/categories")
def get_admin_categories(db: Session = Depends(get_db)):
    return {"categories": []}

@app.get("/api/admin/faqs")
def get_admin_faqs(categoryId: str, db: Session = Depends(get_db)):
    return {"faqs": []}

@app.post("/api/admin/train")
def trigger_training(db: Session = Depends(get_db)):
    res = start_training("manual_trigger")
    return res

@app.get("/")
def read_root():
    return {"status": "ok", "message": "API RAG corriendo exitosamente."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
