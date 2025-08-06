#!/bin/bash
set -e

echo "👔 Starting Manager Enablement Service (Port $PORT)"
echo "📚 Building leaders who lead with fairness and data!"
echo "⚖️ Bias Detection: $BIAS_DETECTION_ENABLED"
echo "🎯 Fair Leadership Algorithms: $FAIRNESS_ALGORITHMS"

echo "⏳ Waiting for ethical algorithms to align..."
sleep 5

echo "🚀 Launching leadership development engine..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
