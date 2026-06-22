CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE students (
student_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
name VARCHAR(100) NOT NULL,
age INT,
gender VARCHAR(10),
family_income_level VARCHAR(20) DEFAULT 'medium',
created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE academic_records (
record_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
student_id UUID REFERENCES students(student_id) ON DELETE CASCADE,
semester INT NOT NULL,
attendance_pct FLOAT NOT NULL,
gpa FLOAT NOT NULL,
assignments_submitted INT DEFAULT 0,
assignments_total INT DEFAULT 10,
recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE risk_assessments (
assessment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
student_id UUID REFERENCES students(student_id) ON DELETE CASCADE,
risk_score FLOAT NOT NULL,
risk_category VARCHAR(10) NOT NULL,
intervention_recommendation TEXT,
assessed_at TIMESTAMP DEFAULT NOW()
);
