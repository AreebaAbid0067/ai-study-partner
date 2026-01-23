from sqlalchemy import Column, String, DateTime, Integer
from dependencies import Base
from datetime import datetime

class Document(Base):
    """Database model for storing document information"""
    
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    uploaded_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Document(id={self.id}, filename={self.filename})>"
