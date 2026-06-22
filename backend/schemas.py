# backend/schemas.py
# FIXED VERSION — accepts simple user-friendly fields from the mobile app
# The predictor.py handles mapping these to the raw dataset features internally

from pydantic import BaseModel
from typing import Optional

class StudentInput(BaseModel):
    student_id:             str
    attendance_pct:         float   # 0-100
    gpa:                    float   # 0-10
    assignments_submitted:  int
    assignments_total:      int
    age:                    int
    family_income_level:    str     # 'low' / 'medium' / 'high'

class PredictionResponse(BaseModel):
    student_id:    str
    risk_score:    float
    risk_category: str
    intervention:  str
    assessed_at:   str

class DashboardStats(BaseModel):
    total:  int
    low:    int
    medium: int
    high:   int