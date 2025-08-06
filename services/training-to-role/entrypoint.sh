#!/bin/bash
set -e

echo "🚀 Starting Training-to-Role Service (Port $PORT)"
echo "📋 Service: $SERVICE_NAME"
echo "🔗 Vault: $VAULT_ADDR"
echo "📨 Kafka: $KAFKA_BOOTSTRAP"
echo "🔐 OPA: $OPA_URL"
echo "🗄️ Database: $DB_NAME"

# Wait for dependencies (optional)
echo "⏳ Waiting for dependencies..."
sleep 5

# Start the application
echo "🎯 Launching FastAPI application..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
