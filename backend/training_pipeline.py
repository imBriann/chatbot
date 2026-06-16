import os
import re
from sqlalchemy.orm import Session
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from database import SessionLocal
from models import Knowledge, Training
import datetime

CHROMA_PERSIST_DIR = os.path.join(os.path.dirname(__file__), "chroma_db_unipamplona")

def clean_text(text: str) -> str:
    # Preprocesamiento y limpieza de datos
    if not text:
        return ""
    text = text.replace('\n', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def start_training(version_name: str = "v1"):
    db: Session = SessionLocal()
    training_run = Training(version=version_name, status="running")
    db.add(training_run)
    db.commit()
    db.refresh(training_run)
    
    try:
        # 1. Recuperar conocimiento de la Base de Datos
        knowledge_items = db.query(Knowledge).filter(Knowledge.is_active == True).all()
        if not knowledge_items:
            raise Exception("No hay datos de conocimiento activos en la base de datos.")
        
        # 2. Convertir a documentos LangChain y Limpieza
        documents = []
        for item in knowledge_items:
            content = f"Pregunta: {clean_text(item.question)}\nRespuesta: {clean_text(item.answer)}"
            doc = Document(page_content=content, metadata={"category": item.category or "general", "id": item.id})
            documents.append(doc)
            
        # 2.5 Cargar también la guía de texto general
        txt_path = os.path.join(os.path.dirname(__file__), "docs", "guia_texto.txt")
        if os.path.exists(txt_path):
            from langchain_community.document_loaders import TextLoader
            loader = TextLoader(txt_path, encoding='utf-8')
            txt_docs = loader.load()
            for t in txt_docs:
                t.metadata["category"] = "general_guide"
            documents.extend(txt_docs)
        
        # 3. Tokenización y partición (Splitting)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(documents)
        
        # 4. Embeddings
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        # 5. Generación y almacenamiento en Vector DB
        vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=embeddings, 
            persist_directory=CHROMA_PERSIST_DIR
        )
        
        training_run.status = "completed"
        training_run.completed_at = datetime.datetime.utcnow()
        training_run.metrics = {"chunks_processed": len(splits), "documents_processed": len(documents)}
        db.commit()
        
        return {"status": "success", "chunks": len(splits), "docs": len(documents)}
        
    except Exception as e:
        training_run.status = "failed"
        training_run.completed_at = datetime.datetime.utcnow()
        training_run.metrics = {"error": str(e)}
        db.commit()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

if __name__ == "__main__":
    print(start_training("test_v1"))
