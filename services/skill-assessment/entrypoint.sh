#!/bin/bash
set -e

echo "🎓 Starting Skill Assessment Service (Port $PORT)"
echo "📚 The skill evaluator that's more accurate than a Swiss chronometer!"
echo "⚖️ Bias Elimination: $BIAS_ELIMINATION"
echo "🧠 Algorithms: $ASSESSMENT_ALGORITHMS"
echo "😂 Fun Fact: We can assess skills better than professors assess term papers!"

echo "⏳ Waiting for the assessment algorithms to calibrate like precision instruments..."
sleep 5

echo "🚀 Launching the merit-based skill evaluation engine..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
