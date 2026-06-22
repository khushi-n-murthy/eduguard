import pandas as pd
import psycopg2

df = pd.read_csv("data/student_dropout_academic_success.csv")

conn = psycopg2.connect(
    host="localhost",
    database="eduguard_db",
    user="eduguard_user",
    password="EduGuard2024!",
    port="5432"
)

cur = conn.cursor()

print("Connected to database")

for i in range(min(100, len(df))):
    cur.execute("""
        INSERT INTO students(name, age, gender, family_income_level)
        VALUES(%s,%s,%s,%s)
    """, (
        f"Student_{i+1}",
        18,
        "Unknown",
        "medium"
    ))

conn.commit()

print("Data inserted successfully!")

cur.close()
conn.close()