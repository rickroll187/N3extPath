#!/bin/bash
set -e

echo "🎯 Starting Hiring Process Service (Port $PORT)"
echo "🏆 The recruitment machine that's fairer than a Supreme Court justice!"
echo "⚖️ Bias Elimination: $BIAS_ELIMINATION"
echo "🎯 Algorithms: $HIRING_ALGORITHMS"
echo "😂 Fun Fact: We can find the perfect candidate, but we still can't explain why printers jam during important presentations!"

echo "⏳ Waiting for the recruitment algorithms to align like hiring stars..."
sleep 5

echo "🚀 Launching the bias-free recruitment engine..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
