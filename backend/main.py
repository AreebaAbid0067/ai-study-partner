from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import documents
from dependencies import init_db

app = FastAPI(title="AI Study Partner API")

# Initialize database
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(documents.router)

@app.get("/checkin")
async def health_check():
    return {"status": "ok"}




