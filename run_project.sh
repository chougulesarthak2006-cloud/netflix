#!/usr/bin/env bash
# ==============================================================================
# run_project.sh - Linux/Ubuntu Interactive Runner for Netflix Big Data Project
# ==============================================================================

echo "==================================================================="
echo "    Netflix Movies and TV Shows Data Analysis (Hadoop and Hive)"
echo "==================================================================="
echo ""
echo "Select Execution Option:"
echo "  [1] Launch Interactive Web Dashboard (Local Demo + Hadoop Cluster)"
echo "  [2] Run Complete Automated CLI Pipeline (HDFS + HiveQL + Charts)"
echo "  [3] Run Hadoop MapReduce Stream Simulation (mapper.py + reducer.py)"
echo "  [4] Execute Real Hadoop Cluster Pipeline (hdfs_commands.sh + Hive)"
echo "  [5] Exit"
echo ""

read -p "Enter choice [1-5] (Default: 1): " choice
choice=${choice:-1}

# Activate virtualenv if available
if [ -d ".venv/bin" ]; then
    source .venv/bin/activate
fi

case $choice in
    1)
        echo "[*] Launching Web Dashboard on http://localhost:5000 ..."
        if command -v xdg-open &> /dev/null; then
            (sleep 1 && xdg-open http://localhost:5000) &
        elif command -v open &> /dev/null; then
            (sleep 1 && open http://localhost:5000) &
        fi
        python3 app.py || python app.py
        ;;
    2)
        echo "[*] Running Automated CLI Pipeline..."
        python3 run_project.py || python run_project.py
        ;;
    3)
        echo "[*] Running MapReduce Stream Simulation..."
        python3 hadoop/run_local_mapreduce.py || python hadoop/run_local_mapreduce.py
        ;;
    4)
        echo "[*] Executing Real Hadoop & Hive Cluster Scripts..."
        cd hdfs && ./hdfs_commands.sh all
        cd ../hive && ./run_all_hive.sh
        ;;
    5)
        echo "Exiting."
        exit 0
        ;;
    *)
        echo "Invalid selection."
        exit 1
        ;;
esac
