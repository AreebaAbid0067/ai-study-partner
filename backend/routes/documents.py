from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import Annotated
import os
import shutil
from datetime import datetime

from dependencies import get_db
from services.document_service import DocumentService
from schemas.document import DocumentResponse, DocumentListResponse, DocumentStats

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_file(
    file: Annotated[UploadFile, File()],
    db: Session = Depends(get_db)
):
    """Upload a document (PDF, TXT, or DOC)"""
    allowed_types = [
        "application/pdf",
        "text/plain",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Supported types: PDF, TXT, DOCX"
        )
    
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Save file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
    file_path = os.path.join("uploads", timestamp + file.filename)
    
    # Copy file to disk
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Get file size
    file_size = os.path.getsize(file_path)
    doc_id = timestamp + file.filename
    
    # Save to database
    from schemas.document import DocumentCreate
    doc_data = DocumentCreate(
        id=doc_id,
        filename=file.filename,
        file_path=file_path,
        file_type=file.content_type,
        file_size=file_size
    )
    
    saved_doc = DocumentService.save_document(db, doc_data)
    
    return {
        "id": saved_doc.id,
        "filename": saved_doc.filename,
        "message": "File uploaded successfully",
        "file_size": saved_doc.file_size
    }


@router.get("/list")
async def list_documents(db: Session = Depends(get_db)) -> DocumentListResponse:
    """Get list of all uploaded documents"""
    documents = DocumentService.get_all_documents(db)
    return DocumentListResponse(
        total=len(documents),
        documents=documents
    )


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: str, db: Session = Depends(get_db)):
    """Get details of a specific document"""
    document = DocumentService.get_document_by_id(db, document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return document


@router.delete("/{document_id}")
async def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document"""
    success = DocumentService.delete_document(db, document_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {"message": "Document deleted successfully", "document_id": document_id}


@router.get("/", response_model=DocumentStats)
async def get_document_stats(db: Session = Depends(get_db)):
    """Get document statistics"""
    total_docs = DocumentService.get_document_count(db)
    total_size = DocumentService.get_total_storage_size(db)
    
    return DocumentStats(
        total_documents=total_docs,
        total_size_bytes=total_size,
        total_size_mb=round(total_size / (1024 * 1024), 2)
    )
