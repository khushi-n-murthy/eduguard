# EduGuard — Predictive Dropout Analytics with Adaptive Intervention Logic

<div align="center">

![EduGuard Banner](https://img.shields.io/badge/EduGuard-Dropout%20Prevention%20AI-8B0000?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=for-the-badge&logo=fastapi)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker)
![AWS](https://img.shields.io/badge/AWS-EC2%20%2B%20RDS-FF9900?style=for-the-badge&logo=amazonaws)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.6.1-F7931E?style=for-the-badge&logo=scikit-learn)
![Expo](https://img.shields.io/badge/Expo-Mobile%20App-000020?style=for-the-badge&logo=expo)

**An AI-driven student dropout prediction system built with a real ML model, containerized backend, cloud database, and a live mobile app — deployable end to end.**

*RV College of Engineering, Bengaluru — Department of Computer Science*

</div>

---

## Table of Contents

- [Overview](#overview)
- [Live Demo](#live-demo)
- [System Architecture](#system-architecture)
- [Team & Task Split](#team--task-split)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [ML Model](#ml-model)
- [Project Structure](#project-structure)
- [Local Development Setup](#local-development-setup)
- [Docker Setup](#docker-setup)
- [AWS Deployment](#aws-deployment)
- [API Reference](#api-reference)
- [Mobile App](#mobile-app)
- [What We Built Manually (No AI)](#what-we-built-manually-no-ai)
- [References](#references)

---

## Overview

EduGuard is an AI-powered student dropout prevention platform that moves beyond simple prediction into **adaptive intervention**. Traditional systems identify at-risk students too late — after repeated failures or prolonged absence. EduGuard detects risk early using a machine learning model trained on real academic data and recommends personalized interventions before dropout occurs.

### The Problem

Educational institutions rely on manual monitoring — slow, inconsistent, and reactive. Factors like low attendance, poor grades, financial stress, and reduced engagement contribute to dropout, but no single system analyses these collectively or acts on them proactively.

### Our Solution

- **Predict** dropout risk using a Random Forest classifier trained on real student data
- **Classify** students into Low / Medium / High risk categories
- **Recommend** specific interventions: counseling, mentoring, financial support
- **Monitor** in real time via a live mobile app and cloud dashboard
- **Scale** from a single institution to district-wide with no architectural changes

---

## Live Demo

| Service | URL |
|---|---|
| API Health Check | `http://13.201.52.51:8000/health` |
| Interactive API Docs | `http://13.201.52.51:8000/docs` |
| Dashboard Stats | `http://13.201.52.51:8000/dashboard/stats` |
| Mobile App | Scan QR via Expo Go (run `npx expo start` in `mobile_app/`) |

> **Note:** The EC2 instance is shut down after the presentation to stay within AWS free tier limits.

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    MOBILE APP (Expo Go)                         │
│              React Native  ·  TypeScript  ·  Expo Router        │
└──────────────────────────┬──────────────────────────────────────┘
                           │ HTTP (port 8000)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│                  AWS EC2 (t3.micro)                              │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              Docker Container                            │   │
│  │   FastAPI  ·  Uvicorn  ·  scikit-learn  ·  SQLAlchemy   │   │
│  │                                                          │   │
│  │   /health  ·  /predict  ·  /dashboard/stats             │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────┬──────────────────────────────────────┘
                           │ SSL (port 5432)
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│              AWS RDS PostgreSQL (db.t3.micro)                    │
│   students  ·  academic_records  ·  risk_assessments            │
└─────────────────────────────────────────────────────────────────┘
```

**Security layers:**
- EC2 Security Group: SSH (port 22, My IP only) + API (port 8000, public)
- RDS Security Group: PostgreSQL (port 5432, EC2 security group only — not public internet)
- IAM: Least-privilege user, no root credentials used
- Docker: Non-root user inside container
- RDS: SSL-only connections (`?sslmode=require`)

---

## Team & Task Split

| Member | Role | Component |
|---|---|---|
| **Khushi N** (Team Lead) | Infrastructure | AWS EC2 + RDS + Docker + Deployment |
| **Nabhanya Agarwal** | Backend & ML | FastAPI Backend + Random Forest Model |
| **Nanditha L** | Frontend | React Native Mobile App (Expo) |
| **Namala Namrata** | Data | PostgreSQL Schema + Seed Data Pipeline |

*Guide: Prof. Nithyashree G D, Assistant Professor, Dept. of Computer Science, RVCE*

---

## Tech Stack

### Backend
- **Python 3.11** — runtime
- **FastAPI 0.111.0** — REST API framework with auto-generated OpenAPI docs
- **Uvicorn** — ASGI server
- **SQLAlchemy 2.0** — ORM for PostgreSQL
- **psycopg2** — PostgreSQL driver
- **scikit-learn 1.6.1** — Random Forest classifier
- **joblib** — model serialization
- **pydantic** — request/response validation

### Infrastructure
- **Docker** — containerization
- **Docker Hub** — container registry (`khushinmurthy/eduguard-api`)
- **AWS EC2 t3.micro** — cloud server (Amazon Linux 2023)
- **AWS RDS PostgreSQL 15** — managed cloud database
- **AWS CloudWatch** — live metrics and monitoring

### Mobile
- **React Native** — cross-platform mobile framework
- **Expo SDK 56** — development platform
- **Expo Router** — file-based navigation
- **TypeScript** — type safety
- **Expo Go** — no-deployment mobile testing

### Database
- **PostgreSQL 15** — primary database (local + AWS RDS)

---

## Dataset

**Source:** [UCI Higher Education Predictors of Student Retention](https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention)

| Property | Value |
|---|---|
| Records | 4,424 students |
| Features | 35 academic, demographic, and socioeconomic columns |
| Target | `Target` — Dropout / Graduate / Enrolled |
| Delimiter | Semicolon (`;`) — important for correct CSV parsing |
| Label encoding | `Dropout` → 1, `Graduate`/`Enrolled` → 0 |

### Feature Mapping

Since this dataset doesn't contain literal "attendance" or "income" columns, we engineered proxies:

| App Input | Source Column(s) | Mapping |
|---|---|---|
| `gpa` | `Curricular units 1st sem (grade)` | Rescaled 0–20 → 0–10 |
| `attendance_pct` | `Curricular units 1st sem (evaluations)` ÷ enrolled | Ratio × 100 |
| `assignment_ratio` | `Curricular units 1st sem (approved)` ÷ enrolled | Direct ratio |
| `age` | `Age at enrollment` | Direct |
| `income_enc` | `Debtor` + `Tuition fees up to date` | 0=low, 1=med, 2=high |
| `dropped_out` | `Target` | Dropout=1, else=0 |

> **Presentation note:** Using academic-performance ratios as attendance proxies is a deliberate, defensible modeling decision — this dataset is Portuguese university data where literal attendance tracking wasn't collected.

---

## ML Model

**Algorithm:** Random Forest Classifier (`scikit-learn 1.6.1`)

```python
RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    class_weight='balanced',  # handles dropout class imbalance
    random_state=42
)
```

**Why Random Forest:**
- High accuracy on mixed tabular features
- Handles imbalanced datasets well (with `class_weight='balanced'`)
- Reduces overfitting compared to a single Decision Tree
- Feature importance is interpretable

**Why `class_weight='balanced'`:**
Dropout is a minority class — students who drop out are fewer than those who graduate. Without this, the model would learn to predict "Graduate" for everyone and appear accurate while missing all actual dropouts.

**Why `stratify=y` in train/test split:**
Preserves the dropout/non-dropout ratio in both training and test sets, ensuring evaluation metrics reflect real-world class distribution.

**Risk Thresholds:**

| Score Range | Category | Intervention |
|---|---|---|
| < 0.35 | 🟢 LOW | Regular check-ins recommended |
| 0.35 – 0.65 | 🟡 MEDIUM | Schedule counseling session this week |
| > 0.65 | 🔴 HIGH | Immediate mentor assignment + parent notification |

---

## Project Structure

```
eduguard/
├── backend/                    # Nabhanya — FastAPI server
│   ├── main.py                 # App entry point, route definitions
│   ├── database.py             # SQLAlchemy engine + session
│   ├── models.py               # ORM table models
│   ├── schemas.py              # Pydantic request/response schemas
│   ├── predictor.py            # Model loading + feature mapping + inference
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Local env vars (never commit)
│   └── .env.example            # Template with placeholder values
│
├── ml_model/                   # Nabhanya — ML training pipeline
│   ├── train_model.ipynb       # Training notebook (EDA → features → export)
│   ├── eduguard_model.pkl      # Exported trained model (share via Drive, not git)
│   ├── seed_data.py            # Ingests CSV into PostgreSQL
│   └── data/
│       └── student_dropout_academic_success.csv   # Kaggle dataset
│
├── database/                   # Namrata — Schema
│   ├── init.sql                # CREATE TABLE statements
│   └── migrations/             # Future schema changes
│
├── mobile_app/                 # Nanditha — Expo React Native app
│   ├── app/                    # Expo Router screens
│   ├── components/             # Reusable UI components
│   ├── constants/              # API URL config
│   ├── hooks/                  # Data fetching hooks
│   ├── src/
│   └── global.css
│
├── docker/                     # Khushi — Containerization
│   ├── Dockerfile              # Multi-layer Python image
│   └── docker-compose.yml      # Local dev: API + DB together
│
├── infra/                      # Khushi — AWS deployment
│   ├── deploy.sh               # One-command redeploy to EC2
│   ├── ec2_setup.sh            # First-time EC2 Docker installation
│   ├── first_run.sh            # Initial container launch on EC2
│   └── aws_setup.md            # AWS configuration notes
│
├── .dockerignore
├── .gitignore
└── README.md
```

---

## Local Development Setup

### Prerequisites
- Python 3.11+
- PostgreSQL 15 (local)
- Node.js 18+ (for mobile app)
- Docker Desktop

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/eduguard.git
cd eduguard
```

### 2. Set up the database

```bash
# Start PostgreSQL and run schema
psql -U postgres -c "CREATE USER eduguard_user WITH PASSWORD 'EduGuard2024!';"
psql -U postgres -c "CREATE DATABASE eduguard_db OWNER eduguard_user;"
psql -U eduguard_user -d eduguard_db -f database/init.sql
```

### 3. Download the dataset and seed data

```bash
# Place the CSV at ml_model/data/student_dropout_academic_success.csv
cd ml_model
pip install pandas psycopg2-binary
python seed_data.py
```

### 4. Train the model

```bash
# Open and run all cells in ml_model/train_model.ipynb
jupyter notebook train_model.ipynb
# This generates eduguard_model.pkl
```

### 5. Run the backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env   # fill in your local values
uvicorn main:app --reload --port 8000
```

Test it:
```bash
curl http://localhost:8000/health
# {"status":"healthy","model":"loaded","version":"1.0.0"}
```

### 6. Run the mobile app

```bash
cd mobile_app
npm install
npx expo start
# Scan QR code with Expo Go on your phone
```

---

## Docker Setup

### Local development (API + DB in containers)

```bash
cd docker
docker-compose up --build
```

Both the API (port 8000) and PostgreSQL (port 5432) start together. The database schema is auto-created from `database/init.sql`.

Test:
```bash
curl http://localhost:8000/health
```

### Build and push image manually

```bash
# From project root
docker build -f docker/Dockerfile -t YOUR_DOCKERHUB_USERNAME/eduguard-api:latest .
docker push YOUR_DOCKERHUB_USERNAME/eduguard-api:latest
```

---

## AWS Deployment

### Infrastructure overview

| Resource | Type | Purpose |
|---|---|---|
| EC2 | t3.micro (Amazon Linux 2023) | Runs Docker container |
| RDS | PostgreSQL 15 db.t3.micro | Production database |
| Security Group `eduguard-ec2-sg` | EC2 firewall | SSH (22, My IP) + API (8000, public) |
| Security Group `eduguard-rds-sg` | RDS firewall | PostgreSQL (5432, EC2 only) |
| CloudWatch | Basic monitoring | Live CPU + network metrics |

### First-time EC2 setup

```bash
# SSH into EC2
ssh -i ~/.ssh/eduguard-key.pem ec2-user@YOUR_EC2_IP

# Run setup script
bash infra/ec2_setup.sh

# Log out and back in (required for docker group change)
exit
ssh -i ~/.ssh/eduguard-key.pem ec2-user@YOUR_EC2_IP

# First run
bash infra/first_run.sh
```

### Redeploy after code changes

```bash
# From your laptop — builds, pushes, and redeploys in one command
bash infra/deploy.sh
```

### Environment variables (set in docker run command)

```bash
DATABASE_URL=postgresql://eduguard_user:PASSWORD@RDS_ENDPOINT:5432/eduguard_db?sslmode=require
MODEL_PATH=/app/ml_model/eduguard_model.pkl
```

---

## API Reference

Base URL: `http://<EC2_PUBLIC_IP>:8000`

Interactive docs: `http://<EC2_PUBLIC_IP>:8000/docs`

### GET /health

Check if the server and model are loaded.

**Response:**
```json
{
  "status": "healthy",
  "model": "loaded",
  "version": "1.0.0"
}
```

### POST /predict

Predict dropout risk for a student.

**Request body:**
```json
{
  "student_id": "demo-001",
  "attendance_pct": 45.0,
  "gpa": 3.5,
  "assignments_submitted": 3,
  "assignments_total": 10,
  "age": 20,
  "family_income_level": "low"
}
```

**Response:**
```json
{
  "student_id": "demo-001",
  "risk_score": 0.737,
  "risk_category": "HIGH",
  "intervention": "Immediate mentor assignment + parent notification",
  "assessed_at": "2026-06-22T02:32:41.912108"
}
```

| Field | Type | Description |
|---|---|---|
| `risk_score` | float | Probability of dropout (0.0 – 1.0) |
| `risk_category` | string | LOW / MEDIUM / HIGH |
| `intervention` | string | Recommended action for teacher/admin |
| `assessed_at` | string | ISO 8601 timestamp |

### GET /dashboard/stats

Aggregate risk counts across all assessments — used by the mobile dashboard.

**Response:**
```json
{
  "total": 45,
  "low": 20,
  "medium": 15,
  "high": 10
}
```

---

## Mobile App

The Expo React Native app runs on classmates' phones via **Expo Go** — no App Store submission or deployment required.

### Screens

**Risk Checker** — Enter a student's attendance %, GPA, and income level. Get an instant risk prediction from the live AWS API with color-coded result (🟢 LOW / 🟡 MEDIUM / 🔴 HIGH) and the recommended intervention.

**Dashboard** — Live aggregate stats pulled from the PostgreSQL database showing how many students have been assessed and their risk distribution. Refreshes on demand.

### Running the app

```bash
cd mobile_app
npm install
npx expo start
```

Scan the QR code with Expo Go. Your phone and the laptop running Expo must be on the same WiFi network, OR the API base URL must point to the public EC2 IP.

### Changing the API URL

Find the constants file (typically `src/constants/` or `constants/`) and update:

```typescript
export const BASE_URL = 'http://13.201.52.51:8000';
```

---

## Database Schema

```sql
-- Students table
CREATE TABLE students (
    student_id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                VARCHAR(100) NOT NULL,
    age                 INT,
    gender              VARCHAR(10),
    family_income_level VARCHAR(20) DEFAULT 'medium',
    created_at          TIMESTAMP DEFAULT NOW()
);

-- Academic records (one per semester per student)
CREATE TABLE academic_records (
    record_id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id             UUID REFERENCES students(student_id) ON DELETE CASCADE,
    semester               INT NOT NULL,
    attendance_pct         FLOAT NOT NULL,
    gpa                    FLOAT NOT NULL,
    assignments_submitted  INT DEFAULT 0,
    assignments_total      INT DEFAULT 10,
    recorded_at            TIMESTAMP DEFAULT NOW()
);

-- Risk assessments (written by API after each /predict call)
CREATE TABLE risk_assessments (
    assessment_id               UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id                  UUID REFERENCES students(student_id) ON DELETE CASCADE,
    risk_score                  FLOAT NOT NULL,
    risk_category               VARCHAR(10) NOT NULL,
    intervention_recommendation TEXT,
    assessed_at                 TIMESTAMP DEFAULT NOW()
);
```

---

## What We Built Manually (No AI)

This project used AI tools to accelerate boilerplate and code generation. These are the engineering decisions and configurations we made ourselves — things AI tools don't do for you:

| Decision | Why It Matters |
|---|---|
| UUID over integer IDs for student records | Portability across institutions — no ID collision risk |
| `class_weight='balanced'` in Random Forest | Dropout is a minority class — without this, the model ignores dropouts |
| `stratify=y` in train/test split | Preserves class distribution so evaluation metrics are valid |
| IAM user with least-privilege access (not root) | Security best practice — root credentials never used for daily operations |
| RDS Security Group: EC2-only access on port 5432 | Database is not accessible from the public internet |
| Docker layer order: requirements before code | Cache invalidation — rebuilds are fast when only code changes, not dependencies |
| Non-root user inside Docker container | Container security — process runs as `appuser`, not root |
| `?sslmode=require` in DATABASE_URL | RDS enforces SSL — discovered and fixed from production error logs |
| t3.micro over t2.micro | t2.micro unavailable in ap-south-1 — recognized and adapted on the fly |
| Feature proxy engineering for UCI dataset | Dataset has no literal attendance/income columns — engineered from curricular unit ratios |
| Scikit-learn + numpy version pinning | Resolved `_loss` module and BitGenerator pickle compatibility errors from production logs |

---

## .gitignore

```
.env
*.pkl
ml_model/data/
__pycache__/
*.pyc
node_modules/
.expo/
dist/
venv/
```

---

## References

1. Berka, P., & Marek, L. (2023). A study on dropout prediction for university students using machine learning. *Applied Sciences*, 13(4), 2156–2171.
2. Albreiki, B., et al. (2023). An explainable machine learning approach for student dropout prediction. *Expert Systems with Applications*, 213, 118979.
3. Silva, C., et al. (2024). Interpretable dropout prediction towards XAI-based personalized intervention. *International Journal of Artificial Intelligence in Education*, 34(2), 455–472.
4. Kloft, M., et al. (2024). Predicting student dropouts with machine learning: An empirical study in higher education. *Technology in Society*, 76, 102410.
5. Scientific Reports (2025). Student dropout prediction through machine learning optimization using Moodle log data. Nature Publishing Group.
6. Scientific Reports (2025). PSO weighted ensemble framework with SMOTE balancing for student dropout prediction. Nature Publishing Group.
7. UCI Machine Learning Repository — Student Dropout Dataset. https://archive.ics.uci.edu
8. Kaggle — Higher Education Predictors of Student Retention. https://www.kaggle.com/datasets/thedevastator/higher-education-predictors-of-student-retention
9. Han, J., Kamber, M., & Pei, J. (2022). *Data Mining: Concepts and Techniques* (4th ed.). Morgan Kaufmann.
10. Géron, A. (2022). *Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.

---

<div align="center">

Built with determination by Team EduGuard — RVCE Bengaluru, 2026

*"Yes, we used AI to accelerate — but here's what AI can't do for you."*

</div>
