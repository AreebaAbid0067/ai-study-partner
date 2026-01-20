from fastapi import APIRouter

router = APIRouter(prefix="/study", tags=["study"])

@router.post("/ask")
async def ask_question(question: str, subject: str):
    # Handle question answering logic
    pass
