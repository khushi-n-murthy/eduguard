"""
Generate synthetic student data for dashboard evaluation.
"""

import random
import json
from predictor import predict

def generate_synthetic_students(count=30):
    """Generate realistic synthetic student data."""
    
    # Set seed for reproducibility
    random.seed(42)
    
    first_names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry",
        "Iris", "Jack", "Karen", "Leo", "Mia", "Noah", "Olivia", "Peter",
        "Quinn", "Rachel", "Sam", "Taylor", "Uma", "Victor", "Wendy", "Xander",
        "Yara", "Zoe", "Adam", "Bella", "Carlos", "Dana"
    ]
    
    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
        "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
        "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin"
    ]
    
    students = []
    
    for i in range(count):
        student = {
            "id": i + 1,
            "name": f"{random.choice(first_names)} {random.choice(last_names)}",
            "age": random.randint(18, 35),
            "attendance_pct": random.randint(60, 100),
            "gpa": round(random.uniform(1.5, 9.5), 2),
            "assignments_submitted": random.randint(3, 12),
            "assignments_total": 12,
            "family_income_level": random.choice(["low", "medium", "high"]),
        }
        
        # Get risk prediction
        risk_score, category, intervention = predict(
            attendance_pct=student["attendance_pct"],
            gpa=student["gpa"],
            assignments_submitted=student["assignments_submitted"],
            assignments_total=student["assignments_total"],
            age=student["age"],
            family_income_level=student["family_income_level"]
        )
        
        student["risk_score"] = round(risk_score, 4)
        student["risk_category"] = category
        student["intervention"] = intervention
        
        students.append(student)
    
    return students


if __name__ == "__main__":
    students = generate_synthetic_students(30)
    print(json.dumps(students, indent=2))
