from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
from celery.result import AsyncResult
from celery_worker import celery_app
from models import SessionLocal, AnalysisResult

app = FastAPI(title="Blood Test Report Analyser")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    try:
        os.makedirs("data", exist_ok=True)
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        if not query:
            query = "Summarise my Blood Test Report"
        # Submit Celery task with file.filename
        task = celery_app.send_task(
            'celery_worker.analyze_blood_report_task',
            args=[query.strip(), file.filename, file_path]
        )
        db = SessionLocal()
        db_result = AnalysisResult(file_name=file.filename, query=query.strip(), analysis="", created_at=None)
        db.add(db_result)
        db.commit()
        db.close()
        return {"status": "processing", "task_id": task.id, "file_processed": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

@app.get("/analyze/status/{task_id}")
def get_analysis_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": "pending"}
    elif task_result.state == 'SUCCESS':
        return {"status": "completed", "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": "failed", "error": str(task_result.info)}
    else:
        return {"status": task_result.state}

@app.get("/results")
def get_all_results():
    db = SessionLocal()
    results = db.query(AnalysisResult).all()
    db.close()
    return [
        {
            "id": r.id,
            "file_name": r.file_name,
            "query": r.query,
            "analysis": r.analysis,
            "created_at": r.created_at
        } for r in results
    ]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)