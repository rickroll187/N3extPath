#!/bin/bash
set -e

echo "🛤️ Starting Learning Path Generator Service (Port $PORT)"
echo "🎯 Your personal career GPS that never asks for directions!"
echo "🧠 Algorithms: $PATH_ALGORITHMS"
echo "⚖️ Personalization: $PERSONALIZATION_ENGINE"
echo "😂 Fun Fact: More reliable than Apple Maps, but for your career!"

echo "⏳ Waiting for the stars to align your learning journey..."
sleep 5

echo "🚀 Launching the career navigation system..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
