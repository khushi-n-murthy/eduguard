from sqlalchemy import Column, String, Float, Integer, Text, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base
import uuid


class Student(Base):
    __tablename__ = 'students'
    student_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    age = Column(Integer)
    gender = Column(String(10))
    family_income_level = Column(String(20), default='medium')
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class AcademicRecord(Base):
    __tablename__ = 'academic_records'
    record_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.student_id'))
    semester = Column(Integer, nullable=False)
    attendance_pct = Column(Float, nullable=False)
    gpa = Column(Float, nullable=False)
    assignments_submitted = Column(Integer, default=0)
    assignments_total = Column(Integer, default=10)
    recorded_at = Column(DateTime(timezone=True), server_default=func.now())


class RiskAssessment(Base):
    __tablename__ = 'risk_assessments'
    assessment_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey('students.student_id'), nullable=True)
    risk_score = Column(Float, nullable=False)
    risk_category = Column(String(10), nullable=False)
    intervention_recommendation = Column(Text)
    assessed_at = Column(DateTime(timezone=True), server_default=func.now())
