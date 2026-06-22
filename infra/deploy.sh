#!/bin/bash
# infra/deploy.sh — run this from your laptop to redeploy the API to EC2
# Usage: bash infra/deploy.sh

set -e  # stop immediately if any command fails

# ── EDIT THESE THREE VALUES ──────────────────────────────────────────────
EC2_IP="YOUR_EC2_IP"
KEY_PATH="$HOME/.ssh/eduguard-key.pem"
RDS_ENDPOINT="YOUR_RDS_ENDPOINT"
DB_PASSWORD="YOUR_DB_PASSWORD"
# ──────────────────────────────────────────────────────────────────────────

IMAGE="eduguard2024/eduguard-api:latest"
DB_URL="postgresql://eduguard_user:${DB_PASSWORD}@${RDS_ENDPOINT}:5432/eduguard_db"

echo "▶ Building new Docker image..."
docker build -f docker/Dockerfile -t "$IMAGE" .

echo "▶ Pushing to Docker Hub..."
docker push "$IMAGE"

echo "▶ Deploying to EC2 ($EC2_IP)..."
ssh -i "$KEY_PATH" -o StrictHostKeyChecking=no ec2-user@"$EC2_IP" \
  "DB_URL='$DB_URL' bash -s" << 'REMOTE_SCRIPT'
  set -e
  echo "  → Pulling latest image..."
  docker pull eduguard2024/eduguard-api:latest

  echo "  → Stopping old container (if any)..."
  docker stop eduguard-api 2>/dev/null || true
  docker rm   eduguard-api 2>/dev/null || true

  echo "  → Starting new container..."
  docker run -d \
    --name eduguard-api \
    --restart unless-stopped \
    -p 8000:8000 \
    -e DATABASE_URL="$DB_URL" \
    -e MODEL_PATH='/app/ml_model/eduguard_model.pkl' \
    eduguard2024/eduguard-api:latest

  echo "  → Recent logs:"
  sleep 3
  docker logs eduguard-api --tail=15
REMOTE_SCRIPT

echo ""
echo "   Done. API live at: http://$EC2_IP:8000"
echo "   Health check:      http://$EC2_IP:8000/health"
echo "   API docs:           http://$EC2_IP:8000/docs"