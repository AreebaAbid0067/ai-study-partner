# Database Setup Guide for AI Study Partner

## What Was Created

I've set up a complete SQLAlchemy database layer for your project with the following files:

### 1. **config.py** - Configuration
Stores database connection string and app settings
- Uses SQLite by default (automatic, no setup needed)
- Can be switched to PostgreSQL by changing `DATABASE_URL`

### 2. **dependencies.py** - Database Connection
Sets up database engine and session management
- `engine`: Database connection pool
- `SessionLocal`: Creates database sessions
- `get_db()`: Dependency injection for routes
- `init_db()`: Creates all tables automatically

### 3. **models/document.py** - Database Schema
Defines the `documents` table structure with columns:
- `id` (primary key)
- `filename`
- `file_path`
- `file_type`
- `file_size`
- `uploaded_at`

### 4. **schemas/document.py** - Data Validation
Pydantic models for API request/response validation:
- `DocumentBase`: Base fields
- `DocumentCreate`: For creating documents
- `DocumentResponse`: For API responses
- `DocumentListResponse`: For list endpoints
- `DocumentStats`: For statistics endpoint

### 5. **services/document_service.py** - Business Logic
Database query operations:
- `save_document()`: Insert document into DB
- `get_all_documents()`: Fetch all documents
- `get_document_by_id()`: Fetch specific document
- `delete_document()`: Delete document
- `get_document_count()`: Count total documents
- `get_total_storage_size()`: Calculate storage usage

### 6. **routes/documents.py** - API Endpoints (Updated)
Now uses the database instead of in-memory storage:
- POST `/documents/upload` - Upload file
- GET `/documents/list` - List all documents
- GET `/documents/{id}` - Get specific document
- DELETE `/documents/{id}` - Delete document
- GET `/documents/` - Get statistics

---

## Setup Instructions

### Step 1: Install Required Packages
Run in terminal from your backend folder:
```bash
pip install -r ../requirements.txt
```

Or install individually:
```bash
pip install sqlalchemy pydantic-settings
```

### Step 2: Run Your Application
```bash
# From backend folder
uvicorn main:app --reload
```

**That's it!** The database will be created automatically on first run.

---

## Database Details

### Default Database (SQLite)
- **Location**: `ai_study_partner.db` (created in backend folder)
- **Advantage**: No setup needed, perfect for development
- **File**: You can see it in your file explorer after first run

### To Switch to PostgreSQL (Production)
If you want to use PostgreSQL later:

1. Install PostgreSQL
2. Create a database: `createdb ai_study_partner`
3. Update `config.py`:
```python
DATABASE_URL = "postgresql://user:password@localhost/ai_study_partner"
```
4. Install driver: `pip install psycopg2`

---

## How It All Works Together

```
User uploads file
        ↓
POST /documents/upload
        ↓
save_document() in routes/documents.py
        ↓
DocumentService.save_document()
        ↓
DocumentCreate schema validates data
        ↓
Document model saves to database
        ↓
Response sent back to user
```

---

## Testing the API

### Upload a file:
```bash
curl -X POST "http://localhost:8000/documents/upload" \
  -F "file=@your_file.pdf"
```

### Get all documents:
```bash
curl "http://localhost:8000/documents/list"
```

### Get statistics:
```bash
curl "http://localhost:8000/documents/"
```

### Delete a document:
```bash
curl -X DELETE "http://localhost:8000/documents/{document_id}"
```

---

## Important Notes

1. **Database migrations**: If you change the Document model, just delete `ai_study_partner.db` and restart - tables are recreated automatically

2. **File storage**: Files are still saved to the `uploads/` folder. Database just tracks metadata

3. **In production**: 
   - Use PostgreSQL instead of SQLite
   - Store files in cloud storage (AWS S3, Azure Blob, etc.)
   - Set `DEBUG = False` in config.py

4. **Error handling**: The code handles all common errors:
   - File type validation
   - File not found errors
   - Database connection issues

---

## Folder Structure Now:
```
backend/
├── config.py                    ← NEW: Database settings
├── dependencies.py              ← NEW: Database connection
├── main.py                      ← UPDATED: Initializes database
├── models/
│   ├── __init__.py
│   └── document.py              ← NEW: Database schema
├── schemas/
│   └── document.py              ← NEW: API data validation
├── services/
│   └── document_service.py      ← NEW: Database queries
├── routes/
│   └── documents.py             ← UPDATED: Uses database
└── uploads/                     ← Created automatically for files
```

---

## What Happens When You Run It

1. ✅ FastAPI starts
2. ✅ `init_db()` creates `ai_study_partner.db`
3. ✅ `documents` table is created automatically
4. ✅ Server ready to accept uploads
5. ✅ All file metadata is saved to database

**You don't need to do anything - it's all automatic!**
