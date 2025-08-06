#!/bin/bash
set -e

echo "🤝 Starting Mentor Matching Service (Port $PORT)"
echo "💕 Where career relationships bloom based on pure skill compatibility!"
echo "🎯 Algorithm: $MATCHING_ALGORITHM"
echo "⚖️ Bias Prevention: $BIAS_PREVENTION"
echo "😂 Fun Fact: Better matchmaking than Tinder, but for your career!"

echo "⏳ Waiting for cosmic alignment of mentor-mentee pairs..."
sleep 5

echo "🚀 Launching the career cupid engine..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
