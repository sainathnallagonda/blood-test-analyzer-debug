from celery import Celery
from models import SessionLocal, AnalysisResult
from utils import save_analysis_to_csv
import os
import datetime

celery_app = Celery(
    'blood_test_analyser',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@celery_app.task
def analyze_blood_report_task(query, file_name, file_path):
    from main import run_crew
    import uuid
    result = run_crew(query, file_path)
    # Save result to DB
    db = SessionLocal()
    # Find the most recent entry for this file and query (status: processing)
    db_result = db.query(AnalysisResult).filter_by(file_name=file_name, query=query).order_by(AnalysisResult.id.desc()).first()
    if db_result:
        db_result.analysis = str(result)
        db_result.created_at = datetime.datetime.utcnow()
        db.commit()
    db.close()
    # Save result to CSV (if result is a list of dicts)
    file_id = os.path.splitext(os.path.basename(file_path))[0].replace('blood_test_report_', '')
    # If result is a string, you may need to parse it to a list of dicts
    if isinstance(result, list) and result and isinstance(result[0], dict):
        save_analysis_to_csv(result, file_id)
    return result
