#!/usr/bin/env bash
# ==============================================================================
# run_dashboard.sh - Linux/Ubuntu Runner for Netflix Big Data Web Dashboard
# ==============================================================================

echo "==================================================================="
echo "  Netflix Big Data Platform: Local Demo & Hadoop Cluster Engine"
echo "==================================================================="
echo ""
echo "[*] Starting Web Dashboard on http://localhost:5000 ..."
echo "[*] Supports Local Demo Mode and Hadoop Cluster Mode"
echo ""

# Activate virtual environment if present
if [ -d ".venv/bin" ]; then
    source .venv/bin/activate
fi

# Try to open default browser in background
if command -v xdg-open &> /dev/null; then
    (sleep 1 && xdg-open http://localhost:5000) &
elif command -v open &> /dev/null; then
    (sleep 1 && open http://localhost:5000) &
fi

python3 app.py || python app.py
