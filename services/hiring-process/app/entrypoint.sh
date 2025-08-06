#!/bin/bash
set -e

echo "📊 Starting Performance Management Service (Port $PORT)"
echo "🎯 The performance tracker that's fairer than a Supreme Court decision!"
echo "⚖️ Bias Elimination: $BIAS_ELIMINATION"
echo "📈 Algorithms: $REVIEW_ALGORITHMS"
echo "😂 Fun Fact: We track performance better than Santa tracks who's naughty or nice!"

echo "⏳ Waiting for the performance algorithms to warm up like a coffee machine..."
sleep 5

echo "🚀 Launching the bias-free performance engine..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
