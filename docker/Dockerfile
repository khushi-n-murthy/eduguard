# docker/Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first — Docker caches this layer
# so re-builds are fast when only application code changes
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend code
COPY backend/ ./backend/
COPY ml_model/eduguard_model.pkl ./ml_model/eduguard_model.pkl

WORKDIR /app/backend

# Security: never run as root in production
RUN useradd -m appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]