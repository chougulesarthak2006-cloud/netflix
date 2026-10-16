#!/usr/bin/env bash
# ==============================================================================
# Script Name: run_all_hive.sh
# Project:     Netflix Movies and TV Shows Data Analysis using Hadoop and Hive
# Description: End-to-end automation runner for executing Hive database creation,
#              external table mapping, data cleaning, and analytical queries.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}===================================================================${NC}"
echo -e "${BLUE}   Apache Hive Pipeline Runner: Netflix Data Analysis Project      ${NC}"
echo -e "${BLUE}===================================================================${NC}"

# Check Hive binary
if ! command -v hive &> /dev/null; then
    echo -e "${RED}[-] Error: 'hive' command not found in PATH.${NC}"
    echo -e "    Please ensure HIVE_HOME is set and added to your PATH in ~/.bashrc."
    exit 1
fi

echo -e "${GREEN}[1/4] Step 1: Creating Database 'netflix_db'...${NC}"
hive -f "${SCRIPT_DIR}/01_create_database.sql"

echo -e "${GREEN}[2/4] Step 2: Creating External Table 'netflix_raw' with OpenCSVSerde...${NC}"
hive -f "${SCRIPT_DIR}/02_create_external_table.sql"

echo -e "${GREEN}[3/4] Step 3: Executing Data Cleaning & Ingesting into 'netflix_cleaned'...${NC}"
hive -f "${SCRIPT_DIR}/03_data_cleaning.sql"

echo -e "${GREEN}[4/4] Step 4: Running 18 Analytical HiveQL Queries...${NC}"
hive -f "${SCRIPT_DIR}/04_analysis_queries.sql"

echo -e "${BLUE}===================================================================${NC}"
echo -e "${GREEN}[+] Hive Data Analysis Pipeline Completed Successfully!${NC}"
echo -e "${BLUE}===================================================================${NC}"
