#!/bin/bash

echo "🧹 Cleaning up existing drift containers..."
docker rm -f drift_a drift_b 2>/dev/null

echo "🐳 Building drift_server_image..."
docker build -t drift_server_image .

echo "🚀 Launching Drift A (Cart A: slow, linear drift on Register 2)..."
docker run -d --name drift_a \
  -e START_REG=0 \
  -e REG_COUNT=5 \
  -e PORT=15021 \
  -e DRIFT_REGISTER=2 \
  -e DRIFT_TYPE=increment \
  -e DRIFT_INTERVAL=3 \
  -e DRIFT_AMOUNT=1 \
  -p 15021:15021 \
  drift_server_image

echo "🚀 Launching Drift B (Cart B: erratic chaos on Register 2)..."
docker run -d --name drift_b \
  -e START_REG=5 \
  -e REG_COUNT=5 \
  -e PORT=15022 \
  -e DRIFT_REGISTER=2 \
  -e DRIFT_TYPE=random \
  -e DRIFT_INTERVAL=2 \
  -e DRIFT_AMOUNT=5 \
  -p 15022:15022 \
  drift_server_image

echo "✅ Drift containers running on ports 15021 (Cart A) and 15022 (Cart B)."
