from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from database import Base
import datetime

class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    conversations = relationship("Conversation", back_populates="user")

class Conversation(Base):
    __tablename__ = "conversaciones"
    id = Column(String, primary_key=True, index=True) # sessionId
    user_id = Column(Integer, ForeignKey("usuarios.id"), nullable=True)
    title = Column(String, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)
    
    user = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation")

class Message(Base):
    __tablename__ = "mensajes"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(String, ForeignKey("conversaciones.id"))
    sender = Column(String) # 'user' o 'bot'
    text = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    intent = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    related_docs = Column(JSON, nullable=True)
    
    conversation = relationship("Conversation", back_populates="messages")

class Knowledge(Base):
    __tablename__ = "conocimiento"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

class Intent(Base):
    __tablename__ = "intenciones"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    description = Column(Text, nullable=True)
    examples = Column(JSON) # List of example phrases
    
class Training(Base):
    __tablename__ = "entrenamiento"
    id = Column(Integer, primary_key=True, index=True)
    version = Column(String)
    status = Column(String) # 'pending', 'running', 'completed', 'failed'
    metrics = Column(JSON, nullable=True)
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

class Metric(Base):
    __tablename__ = "metricas"
    id = Column(Integer, primary_key=True, index=True)
    metric_type = Column(String, index=True) # e.g. 'api_calls', 'unanswered_questions', 'latency'
    value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
