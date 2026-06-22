#!/bin/bash
# infra/first_run.sh
# The very first time you run the container on EC2 (manual, one-time).
# After this, use deploy.sh for all future updates.
#
# Run this ON THE EC2 INSTANCE after SSH-ing in and after ec2_setup.sh has completed.

set -e

# ── EDIT THESE VALUES before running ─────────────────────────────────────
RDS_ENDPOINT="YOUR_RDS_ENDPOINT"
# e.g. eduguard-db.abcdefg1234.us-east-1.rds.amazonaws.com
DB_PASSWORD="YOUR_DB_PASSWORD"
# ─────────────────────────────────────────────────────────────────────────

DB_URL="postgresql://eduguard_user:${DB_PASSWORD}@${RDS_ENDPOINT}:5432/eduguard_db"

echo "▶ Logging in to Docker Hub (enter your Docker Hub credentials when asked)..."
docker login

echo "▶ Pulling the EduGuard API image..."
docker pull eduguard2024/eduguard-api:latest

echo "▶ Starting the container..."
docker run -d \
  --name eduguard-api \
  --restart unless-stopped \
  -p 8000:8000 \
  -e DATABASE_URL="$DB_URL" \
  -e MODEL_PATH='/app/ml_model/eduguard_model.pkl' \
  eduguard2024/eduguard-api:latest

echo "▶ Waiting for startup..."
sleep 4

echo "▶ Checking container status..."
docker ps

echo "▶ Recent logs:"
docker logs eduguard-api --tail=20

echo ""
echo "▶ Testing health endpoint locally on EC2..."
curl -s http://localhost:8000/health
echo ""
echo ""
echo "✅ If you saw {\"status\":\"healthy\"} above, you're live!"
echo "   Now test from YOUR LAPTOP (not EC2):"
echo "   curl http://<EC2_PUBLIC_IP>:8000/health"