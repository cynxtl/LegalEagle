"""
SQLAlchemy database models for LegalEagle SQLite database.
"""
from datetime import datetime
import uuid

from sqlalchemy import Column, String, Integer, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from backend.app.db.database import Base


class ThreadDB(Base):
    """Chat thread table."""
    __tablename__ = "threads"

    id = Column(String, primary_key=True, default=lambda: f"t-{uuid.uuid4().hex[:8]}")
    title = Column(String, nullable=False, default="New Consultation")
    category = Column(String, nullable=False, default="General")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    messages = relationship("MessageDB", back_populates="thread", cascade="all, delete-orphan", order_by="MessageDB.created_at")


class MessageDB(Base):
    """Chat message table."""
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: f"msg-{uuid.uuid4().hex[:10]}")
    thread_id = Column(String, ForeignKey("threads.id", ondelete="CASCADE"), nullable=False)
    role = Column(String, nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    category = Column(String, nullable=True)
    confidence = Column(String, nullable=True, default="medium")
    sources_json = Column(Text, nullable=True, default="[]")  # Serialized list of Source dicts
    created_at = Column(DateTime, default=datetime.utcnow)

    thread = relationship("ThreadDB", back_populates="messages")


class DocumentDB(Base):
    """Uploaded document table."""
    __tablename__ = "documents"

    id = Column(String, primary_key=True, default=lambda: f"doc-{uuid.uuid4().hex[:8]}")
    name = Column(String, nullable=False)
    size = Column(String, nullable=False)
    pages = Column(Integer, default=1)
    status = Column(String, default="indexed")  # 'indexed', 'processing', 'failed'
    chunk_count = Column(Integer, default=0)
    category = Column(String, default="Contract")
    uploaded_at = Column(DateTime, default=datetime.utcnow)


class SourceDB(Base):
    """Saved & retrieved legal citations table."""
    __tablename__ = "sources"

    id = Column(String, primary_key=True, default=lambda: f"src-{uuid.uuid4().hex[:8]}")
    thread_id = Column(String, nullable=True)
    title = Column(String, nullable=False, default="Retrieved Document")
    citation = Column(String, nullable=True)
    jurisdiction = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    excerpt = Column(Text, nullable=False)
    url = Column(String, nullable=True)
    doc_type = Column(String, default="retrieved_chunk")
    score = Column(Float, nullable=True)
    is_starred = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
