from sqlalchemy.orm import Session
from sqlalchemy import func
from models.document import Document
from schemas.document import DocumentCreate, DocumentResponse
import os

class DocumentService:
    """Service layer for document database operations"""
    
    @staticmethod
    def save_document(db: Session, doc_data: DocumentCreate) -> DocumentResponse:
        """
        Save document details to database
        
        Args:
            db: Database session
            doc_data: DocumentCreate schema with file info
            
        Returns:
            DocumentResponse with saved document details
        """
        db_document = Document(**doc_data.dict())
        db.add(db_document)
        db.commit()
        db.refresh(db_document)
        return DocumentResponse.from_orm(db_document)
    
    @staticmethod
    def get_all_documents(db: Session) -> list[DocumentResponse]:
        """
        Retrieve all documents from database
        
        Args:
            db: Database session
            
        Returns:
            List of DocumentResponse objects
        """
        documents = db.query(Document).all()
        return [DocumentResponse.from_orm(doc) for doc in documents]
    
    @staticmethod
    def get_document_by_id(db: Session, document_id: str) -> DocumentResponse:
        """
        Retrieve a specific document by ID
        
        Args:
            db: Database session
            document_id: ID of the document
            
        Returns:
            DocumentResponse or None if not found
        """
        document = db.query(Document).filter(Document.id == document_id).first()
        return DocumentResponse.from_orm(document) if document else None
    
    @staticmethod
    def delete_document(db: Session, document_id: str) -> bool:
        """
        Delete a document from database and filesystem
        
        Args:
            db: Database session
            document_id: ID of the document to delete
            
        Returns:
            True if successful, False if not found
        """
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            return False
        
        # Delete file from disk
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        db.delete(document)
        db.commit()
        return True
    
    @staticmethod
    def get_document_count(db: Session) -> int:
        """Get total number of documents"""
        return db.query(func.count(Document.id)).scalar()
    
    @staticmethod
    def get_total_storage_size(db: Session) -> int:
        """Get total storage size in bytes"""
        result = db.query(func.sum(Document.file_size)).scalar()
        return result or 0
    
    @staticmethod
    def document_exists(db: Session, document_id: str) -> bool:
        """Check if document exists in database"""
        return db.query(Document).filter(Document.id == document_id).first() is not None
