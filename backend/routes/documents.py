from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import Annotated

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/upload")
async def upload_file(file: Annotated[UploadFile, File()]):
    if file.content_type not in ["application/pdf", "text/plain", "application/msword"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
        # this is also an exception so if u put try catch...the exception 
        # block will take it as exception and instead of displaying this message it will 
        # display the message in the exception block u wrote
    
    return {"filename": file.filename,
            "message":"file uploaded successfully"}





