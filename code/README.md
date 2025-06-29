# Blood Test Report Analyser

A FastAPI-based system for analyzing blood test reports using CrewAI, with background processing via Celery and Redis, and persistent storage of results in SQLite.

---

## 🐞 Bugs Found & How They Were Fixed

- **Import Errors:**
  - Fixed incorrect imports (e.g., `from crewai.agents import Agent` to `from crewai import Agent`).
  - Removed undefined imports (e.g., `search_tool`).
- **Task Validation Errors:**
  - Removed or fixed invalid `tools` arguments in Task definitions to resolve Pydantic validation errors.
- **Dependency Issues:**
  - Cleaned up `requirements.txt` to include only necessary packages.
  - Installed missing runtime dependencies (e.g., `python-multipart`).
- **FastAPI Server Startup:**
  - Removed `reload=True` from `uvicorn.run` in `main.py` for compatibility.
- **File Handling:**
  - Ensured uploaded files are saved with unique names and cleaned up after processing.
- **Celery Integration:**
  - Fixed argument passing to Celery tasks to ensure analysis results are saved in the database.
- **Database Integration:**
  - Added SQLAlchemy models and ensured results are stored and retrievable.

---

## 🚀 Setup & Usage Instructions

### 1. Clone the Repository
```
git clone <your-repo-link>
cd blood-test-analyser-debug
```

### 2. Install Python Dependencies
```
pip install -r requirements.txt
```

### 3. Install & Start Redis
- **Windows:** Download from https://github.com/tporadowski/redis/releases, extract, and run `redis-server.exe`.
- **Linux/Mac:**
  ```
  sudo apt install redis-server
  redis-server
  ```

### 4. Start the Celery Worker
```
celery -A celery_worker.celery_app worker --loglevel=info
```

### 5. Start the FastAPI Server
```
python main.py
```

### 6. Access the API
- Open your browser to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for Swagger UI.

---

## 📑 API Documentation

### **Health Check**
- **GET /**
  - Returns: `{ "message": "Blood Test Report Analyser API is running" }`

### **Analyze Blood Report**
- **POST /analyze**
  - **Form Data:**
    - `file`: PDF file to upload
    - `query`: (optional) Query string for analysis
  - **Response:**
    - `{ "status": "processing", "task_id": "...", "file_processed": "..." }`

### **Check Analysis Status**
- **GET /analyze/status/{task_id}**
  - **Response:**
    - `{ "status": "pending" }` (if still processing)
    - `{ "status": "completed", "result": "..." }` (if done)
    - `{ "status": "failed", "error": "..." }` (if error)

### **Get All Results**
- **GET /results**
  - **Response:**
    - List of all analysis results with fields: `id`, `file_name`, `query`, `analysis`, `created_at`

---

## 📝 Notes
- Uploaded files are saved temporarily and deleted after processing.
- All analysis results are stored in `analysis_results.db` (SQLite).
- For any issues, check the logs of the FastAPI server and Celery worker.

---

## 📬 Submission
- Ensure your repository contains only the necessary code, this README, and a `.gitignore` for Python/SQLite/OS files.
- Push to GitHub and submit your repository link.
