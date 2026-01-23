from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DocumentBase(BaseModel):
    """Base schema for documents"""
    filename: str
    file_type: str
    file_size: int

class DocumentCreate(DocumentBase):
    """Schema for creating a document"""
    file_path: str
    id: str

class DocumentResponse(DocumentBase):
    """Schema for document response"""
    id: str
    uploaded_at: datetime
    
    class Config:
        from_attributes = True  # Allows reading from SQLAlchemy models

class DocumentListResponse(BaseModel):
    """Schema for list of documents"""
    total: int
    documents: list[DocumentResponse]

class DocumentStats(BaseModel):
    """Schema for document statistics"""
    total_documents: int
    total_size_bytes: int
    total_size_mb: float
