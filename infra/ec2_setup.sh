#!/bin/bash
# infra/ec2_setup.sh
# Run this ONCE on a fresh EC2 instance, right after your first SSH login.
# Usage (on EC2, after SSH-ing in):
#   curl -o ec2_setup.sh https://raw.githubusercontent.com/YOUR_REPO/main/infra/ec2_setup.sh
#   bash ec2_setup.sh
# OR just copy-paste this file's contents directly into the EC2 terminal.

set -e

echo "▶ Updating system packages..."
sudo yum update -y

echo "▶ Installing Docker..."
sudo yum install docker -y

echo "▶ Starting Docker and enabling it on boot..."
sudo systemctl start docker
sudo systemctl enable docker

echo "▶ Adding ec2-user to docker group (avoids needing sudo for docker commands)..."
sudo usermod -aG docker ec2-user

echo ""
echo "✅ Docker installed successfully."
echo "⚠  IMPORTANT: log out and log back in now for the group change to apply:"
echo "    exit"
echo "    ssh -i your-key.pem ec2-user@YOUR_EC2_IP"
echo ""
echo "Then verify with: docker --version"