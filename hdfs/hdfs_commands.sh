#!/usr/bin/env bash
# ==============================================================================
# Script Name: hdfs_commands.sh
# Project:     Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
# Description: Automated shell script for managing HDFS operations, starting
#              Hadoop daemons, uploading datasets, and verifying directory status.
# Target OS:   Linux / Ubuntu (Hadoop 2.x / 3.x)
# ==============================================================================

# Exit immediately if a command exits with a non-zero status during critical steps
set -e

# ==========================================
# 1. Configurable Environment Variables
# ==========================================
# The username defaults to the current logged-in user ($USER) or "hadoop"
HADOOP_USER="${HADOOP_USER:-$USER}"
HDFS_BASE_DIR="/user/${HADOOP_USER}"
HDFS_NETFLIX_DIR="${HDFS_BASE_DIR}/netflix"
LOCAL_DATASET_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../dataset" && pwd)"
LOCAL_CSV_FILE="${LOCAL_DATASET_DIR}/netflix_titles.csv"

# Print colored banners for readability
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}===================================================================${NC}"
echo -e "${BLUE}  Hadoop HDFS Management Script: Netflix Big Data Micro-Project   ${NC}"
echo -e "${BLUE}===================================================================${NC}"
echo -e "Configured User:            ${YELLOW}${HADOOP_USER}${NC}"
echo -e "Target HDFS Directory:      ${YELLOW}${HDFS_NETFLIX_DIR}${NC}"
echo -e "Local Dataset File:         ${YELLOW}${LOCAL_CSV_FILE}${NC}"
echo "-------------------------------------------------------------------"

# Function: Display usage menu
show_help() {
    echo "Usage: ./hdfs_commands.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start       - Start Hadoop HDFS and YARN daemons"
    echo "  status      - Check active Hadoop services (jps & dfsadmin)"
    echo "  mkdir       - Create the target HDFS directory"
    echo "  upload      - Upload netflix_titles.csv to HDFS"
    echo "  list        - List files in target HDFS directory"
    echo "  check       - Inspect the uploaded file header and line count"
    echo "  remove      - Remove the dataset from HDFS"
    echo "  all         - Run the complete sequence: mkdir -> upload -> list -> check"
    echo ""
    echo "Examples:"
    echo "  ./hdfs_commands.sh all"
    echo "  HADOOP_USER=hadoop ./hdfs_commands.sh upload"
}

# 1. Start Hadoop Services
start_hadoop() {
    echo -e "${GREEN}[1/7] Starting Hadoop Daemons (HDFS & YARN)...${NC}"
    if command -v start-dfs.sh &> /dev/null; then
        start-dfs.sh
        start-yarn.sh
        echo -e "${GREEN}[+] Hadoop services started successfully.${NC}"
    else
        echo -e "${YELLOW}[!] 'start-dfs.sh' not found in PATH.${NC}"
        echo -e "    Please ensure HADOOP_HOME is set in your ~/.bashrc. Skipping daemon launch."
    fi
}

# 2. Check Hadoop Status
check_status() {
    echo -e "${GREEN}[2/7] Checking Hadoop Daemon Status via jps...${NC}"
    if command -v jps &> /dev/null; then
        jps
        echo "-------------------------------------------------------------------"
        echo "Expected daemons in a single-node Hadoop cluster:"
        echo "  - NameNode"
        echo "  - DataNode"
        echo "  - SecondaryNameNode"
        echo "  - ResourceManager"
        echo "  - NodeManager"
        echo "-------------------------------------------------------------------"
    else
        echo -e "${YELLOW}[!] 'jps' command not found. Ensure Java JDK is on your PATH.${NC}"
    fi

    echo -e "${GREEN}[*] HDFS Health Summary:${NC}"
    hdfs dfsadmin -report -live 2>/dev/null || echo -e "${YELLOW}(hdfs dfsadmin report skipped or namenode is initializing)${NC}"
}

# 3. Create HDFS Directory
create_hdfs_dir() {
    echo -e "${GREEN}[3/7] Creating HDFS Directory: ${HDFS_NETFLIX_DIR}...${NC}"
    # -p creates parent directories as needed without failing if they already exist
    hdfs dfs -mkdir -p "${HDFS_NETFLIX_DIR}"
    echo -e "${GREEN}[+] HDFS directory verified: ${HDFS_NETFLIX_DIR}${NC}"
}

# 4. Upload Dataset to HDFS
upload_dataset() {
    echo -e "${GREEN}[4/7] Uploading Dataset to HDFS...${NC}"
    if [ ! -f "${LOCAL_CSV_FILE}" ]; then
        echo -e "${RED}[-] Local dataset not found at: ${LOCAL_CSV_FILE}${NC}"
        echo -e "    Please run 'python dataset/download_dataset.py' first."
        exit 1
    fi

    echo "Uploading ${LOCAL_CSV_FILE} -> ${HDFS_NETFLIX_DIR}/"
    # -f overwrites destination if it already exists
    hdfs dfs -put -f "${LOCAL_CSV_FILE}" "${HDFS_NETFLIX_DIR}/"
    echo -e "${GREEN}[+] File uploaded successfully to HDFS!${NC}"
}

# 5. List HDFS Files
list_hdfs_files() {
    echo -e "${GREEN}[5/7] Listing files in ${HDFS_NETFLIX_DIR}...${NC}"
    hdfs dfs -ls -h "${HDFS_NETFLIX_DIR}"
}

# 6. Check Dataset Content
check_dataset() {
    echo -e "${GREEN}[6/7] Inspecting first 10 rows of dataset in HDFS...${NC}"
    # Read the top of the file directly from HDFS
    hdfs dfs -cat "${HDFS_NETFLIX_DIR}/netflix_titles.csv" | head -n 10
    echo ""
    echo -e "${GREEN}[*] Verifying total line count in HDFS...${NC}"
    hdfs dfs -cat "${HDFS_NETFLIX_DIR}/netflix_titles.csv" | wc -l
}

# 7. Remove/Replace Dataset
remove_dataset() {
    echo -e "${YELLOW}[7/7] Removing dataset from HDFS...${NC}"
    hdfs dfs -rm -r -skipTrash "${HDFS_NETFLIX_DIR}" || true
    echo -e "${GREEN}[+] HDFS directory ${HDFS_NETFLIX_DIR} removed.${NC}"
}

# ==========================================
# Dispatcher Logic based on arguments
# ==========================================
ACTION="${1:-all}"

case "${ACTION}" in
    start)
        start_hadoop
        ;;
    status)
        check_status
        ;;
    mkdir)
        create_hdfs_dir
        ;;
    upload)
        upload_dataset
        ;;
    list)
        list_hdfs_files
        ;;
    check)
        check_dataset
        ;;
    remove|clean)
        remove_dataset
        ;;
    all)
        echo -e "${BLUE}Running Complete HDFS Workflow...${NC}"
        create_hdfs_dir
        upload_dataset
        list_hdfs_files
        check_dataset
        echo -e "${GREEN}===================================================================${NC}"
        echo -e "${GREEN}[+] HDFS Setup Complete! Data is ready for Hive ingestion.${NC}"
        echo -e "${GREEN}===================================================================${NC}"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo -e "${RED}Unknown command: ${ACTION}${NC}"
        show_help
        exit 1
        ;;
esac
