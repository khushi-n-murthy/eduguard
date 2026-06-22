from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
import uuid
import os

from database import get_db, engine
from models import Base, RiskAssessment
from schemas import StudentInput, PredictionResponse, DashboardStats
from predictor import predict
from generate_students import generate_synthetic_students

Base.metadata.create_all(bind=engine)

app = FastAPI(title='EduGuard API', version='1.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/health')
def health():
    return {'status': 'healthy', 'model': 'loaded', 'version': '1.0.0'}


@app.post('/predict', response_model=PredictionResponse)
def predict_dropout(student: StudentInput, db: Session = Depends(get_db)):
    risk_score, category, intervention = predict(
        attendance_pct=student.attendance_pct,
        gpa=student.gpa,
        assignments_submitted=student.assignments_submitted,
        assignments_total=student.assignments_total,
        age=student.age,
        family_income_level=student.family_income_level
    )
    record = RiskAssessment(
        assessment_id=uuid.uuid4(),
        student_id=None,
        risk_score=round(risk_score, 4),
        risk_category=category,
        intervention_recommendation=intervention
    )
    db.add(record)
    db.commit()
    return PredictionResponse(
        student_id=student.student_id,
        risk_score=round(risk_score, 3),
        risk_category=category,
        intervention=intervention,
        assessed_at=datetime.now().isoformat()
    )


@app.get('/dashboard/stats', response_model=DashboardStats)
def dashboard_stats(db: Session = Depends(get_db)):
    rows = db.query(RiskAssessment.risk_category,
                    func.count().label('cnt')) \
        .group_by(RiskAssessment.risk_category).all()
    counts = {r.risk_category: r.cnt for r in rows}
    return DashboardStats(
        total=sum(counts.values()),
        low=counts.get('LOW', 0),
        medium=counts.get('MEDIUM', 0),
        high=counts.get('HIGH', 0)
    )


@app.get('/api/students')
def list_students():
    """Return synthetic student data with risk assessments."""
    return generate_synthetic_students(30)


@app.get('/')
def serve_dashboard():
    """Serve the teacher dashboard."""
    dashboard_path = os.path.join(os.path.dirname(__file__), 'dashboard.html')
    return FileResponse(dashboard_path, media_type='text/html')
