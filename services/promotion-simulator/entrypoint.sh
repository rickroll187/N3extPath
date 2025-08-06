#!/bin/bash
set -e

echo "🎯 Starting Promotion Simulator Service (Port $PORT)"
echo "🔮 Ready to predict promotions like a crystal ball!"
echo "📊 Algorithms: $SIMULATION_ALGORITHMS"
echo "🗄️ Database: $DB_NAME"

# Wait for dependencies because patience is a virtue
echo "⏳ Waiting for the stars to align..."
sleep 5

echo "🚀 Launching promotion prediction engine..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
