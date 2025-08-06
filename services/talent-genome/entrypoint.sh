#!/bin/bash
set -e

echo "🧬 Starting Talent Genome Service (Port $PORT)"
echo "🔬 Sequencing careers with more precision than actual DNA analysis!"
echo "⚖️ Bias Elimination: $BIAS_ELIMINATION"
echo "🎯 Algorithms: $GENOME_ALGORITHMS"
echo "😂 Fun Fact: We can predict career success, but we still can't predict why printers never work!"

echo "⏳ Waiting for the genetic algorithms to align..."
sleep 5

echo "🚀 Launching the career DNA sequencer..."
uvicorn app.main:app --host 0.0.0.0 --port $PORT --reload --log-level info
