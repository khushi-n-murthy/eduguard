# backend/predictor.py
# FIXED VERSION
#
# The model was trained on ALL 35 raw Kaggle columns.
# The mobile app sends only 6 simple user-friendly fields.
# This file bridges the gap by mapping the 6 simple fields
# to realistic default values for all 35 model features,
# while using the meaningful ones (gpa, age, attendance proxy)
# where they actually map.
#
# Feature order matches the training data column order exactly:
# Marital status, Application mode, Application order, Course,
# Daytime/evening attendance, Previous qualification,
# Previous qualification (grade), Nacionality,
# Mother's qualification, Father's qualification,
# Mother's occupation, Father's occupation, Admission grade,
# Displaced, Educational special needs, Debtor,
# Tuition fees up to date, Gender, Scholarship holder,
# Age at enrollment, International,
# Curricular units 1st sem (credited/enrolled/evaluations/approved/grade/without evaluations),
# Curricular units 2nd sem (credited/enrolled/evaluations/approved/grade/without evaluations),
# Unemployment rate, Inflation rate, GDP

import joblib
import numpy as np
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), '../ml_model/eduguard_model.pkl')
_model = None

def get_model():
    global _model
    if _model is None:
        _model = joblib.load(MODEL_PATH)
    return _model

INCOME_MAP = {'low': 0, 'medium': 1, 'high': 2}

def predict(attendance_pct, gpa, assignments_submitted,
            assignments_total, age, family_income_level):

    model = get_model()

    # --- Derive internal values from simple inputs ---

    # gpa: convert from 0-10 scale back to 0-20 (Portuguese system the model trained on)
    cu1_grade = (gpa / 10) * 20

    # assignment ratio proxy for cu1 approved/enrolled
    ratio = assignments_submitted / max(assignments_total, 1)
    cu1_enrolled    = 6                          # typical semester load
    cu1_approved    = round(ratio * cu1_enrolled)
    cu1_evaluations = assignments_submitted

    # attendance_pct proxy for cu1 evaluations taken vs enrolled
    # reverse: evaluations = (attendance_pct/100) * 1.5 * enrolled
    cu1_evaluations_proxy = round((attendance_pct / 100) * 1.5 * cu1_enrolled)
    cu1_evaluations = max(cu1_evaluations, cu1_evaluations_proxy)

    # income -> debtor and tuition fees proxy
    income_enc = INCOME_MAP.get(family_income_level.lower(), 1)
    debtor          = 1 if income_enc == 0 else 0
    tuition_ok      = 1 if income_enc >= 1 else 0

    # 2nd semester — mirror 1st semester (reasonable default)
    cu2_grade           = cu1_grade
    cu2_enrolled        = cu1_enrolled
    cu2_approved        = cu1_approved
    cu2_evaluations     = cu1_evaluations

    # Economic defaults — use neutral/average values
    # (these matter less since they're the same for all students at a point in time)
    unemployment_rate = 10.8    # approximate average in the dataset
    inflation_rate    = 1.4
    gdp               = 1.74

    # Build the full 35-feature vector in the exact training column order:
    features = np.array([[
        1,                      # Marital status (1=single, most common)
        1,                      # Application mode (1=1st phase general)
        1,                      # Application order
        9238,                   # Course (most common in dataset)
        1,                      # Daytime/evening attendance (1=daytime)
        1,                      # Previous qualification (1=secondary education)
        float(cu1_grade),       # Previous qualification grade (proxy)
        1,                      # Nacionality (1=Portuguese)
        1,                      # Mother's qualification
        1,                      # Father's qualification
        0,                      # Mother's occupation
        0,                      # Father's occupation
        float(cu1_grade),       # Admission grade (proxy from gpa)
        0,                      # Displaced
        0,                      # Educational special needs
        debtor,                 # Debtor ← from income level
        tuition_ok,             # Tuition fees up to date ← from income level
        1,                      # Gender (1=male, neutral default)
        0,                      # Scholarship holder
        age,                    # Age at enrollment ← direct
        0,                      # International
        0,                      # CU1 credited
        cu1_enrolled,           # CU1 enrolled ← derived
        cu1_evaluations,        # CU1 evaluations ← derived from attendance
        cu1_approved,           # CU1 approved ← derived from assignment ratio
        float(cu1_grade),       # CU1 grade ← from gpa
        0,                      # CU1 without evaluations
        0,                      # CU2 credited
        cu2_enrolled,           # CU2 enrolled
        cu2_evaluations,        # CU2 evaluations
        cu2_approved,           # CU2 approved
        float(cu2_grade),       # CU2 grade
        0,                      # CU2 without evaluations
        unemployment_rate,      # Unemployment rate
        inflation_rate,         # Inflation rate
        gdp,                    # GDP
    ]])

    risk_score = float(model.predict_proba(features)[0][1])

    if risk_score < 0.35:
        category     = 'LOW'
        intervention = 'Regular check-ins recommended'
    elif risk_score < 0.65:
        category     = 'MEDIUM'
        intervention = 'Schedule counseling session this week'
    else:
        category     = 'HIGH'
        intervention = 'Immediate mentor assignment + parent notification'

    return risk_score, category, intervention