#!/usr/bin/env python3
"""
run_local_mapreduce.py
----------------------
Executes the Hadoop MapReduce pipeline locally using Python stream processing.
Simulates:
  Step 1: Input Splits
  Step 2: Map Phase (mapper.py)
  Step 3: Shuffle and Sort Phase
  Step 4: Reduce Phase (reducer.py)

This allows students to demonstrate and explain actual MapReduce mechanics
even on machines without Hadoop pre-installed (Local Demo Mode).
"""

import os
import sys
import subprocess

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_PATH = os.path.join(PROJECT_ROOT, "dataset", "netflix_titles.csv")
MAPPER_PY = os.path.join(PROJECT_ROOT, "hadoop", "mapper.py")
REDUCER_PY = os.path.join(PROJECT_ROOT, "hadoop", "reducer.py")
MAPPER_GENRE_PY = os.path.join(PROJECT_ROOT, "hadoop", "mapper_genre.py")
REDUCER_GENRE_PY = os.path.join(PROJECT_ROOT, "hadoop", "reducer_genre.py")

CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"

def run_pipeline(name, mapper_script, reducer_script, input_csv, limit=15):
    print(f"\n{BOLD}{CYAN}=== RUNNING MAPREDUCE JOB: {name} ==={RESET}")
    print(f"1. Input Split : {input_csv} ({os.path.getsize(input_csv):,} bytes)")
    print(f"2. Map Phase    : {mapper_script}")
    print(f"3. Shuffle/Sort : In-memory / Stream sort by Key")
    print(f"4. Reduce Phase : {reducer_script}\n")

    # Step 1 & 2: Map
    with open(input_csv, 'r', encoding='utf-8', errors='replace') as f:
        map_proc = subprocess.Popen(
            [sys.executable, mapper_script],
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        map_out, map_err = map_proc.communicate()

    if map_err:
        print(f"Mapper stderr: {map_err}")

    mapped_lines = [line for line in map_out.strip().split("\n") if line]
    print(f"{GREEN}[+] Map Phase Complete:{RESET} Emitted {len(mapped_lines):,} key-value pairs.")
    print("    Sample Mapped Output:")
    for l in mapped_lines[:5]:
        print(f"      {l}")

    # Step 3: Shuffle & Sort
    print(f"\n{YELLOW}[*] Shuffle & Sort Phase:{RESET} Sorting key-value pairs...")
    sorted_lines = sorted(mapped_lines)
    sorted_input = "\n".join(sorted_lines) + "\n"

    # Step 4: Reduce
    red_proc = subprocess.Popen(
        [sys.executable, reducer_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    red_out, red_err = red_proc.communicate(input=sorted_input)
    if red_err:
        print(f"Reducer stderr: {red_err}")

    reduced_lines = [line for line in red_out.strip().split("\n") if line]
    print(f"{GREEN}[+] Reduce Phase Complete:{RESET} Produced {len(reduced_lines):,} aggregated records.\n")
    print(f"{BOLD}Aggregated Results (Top {limit}):{RESET}")
    print("-" * 55)
    for l in reduced_lines[:limit]:
        parts = l.split("\t")
        if len(parts) == 3:
            print(f"  {parts[0]:<12} | {parts[1]:<25} | {parts[2]:>6}")
        elif len(parts) == 2:
            print(f"  {parts[0]:<35} | {parts[1]:>8}")
    print("-" * 55)
    return reduced_lines

if __name__ == "__main__":
    if not os.path.exists(DATASET_PATH):
        print(f"Dataset not found at {DATASET_PATH}")
        sys.exit(1)

    print(f"{BOLD}{GREEN}Hadoop MapReduce Simulation (Local Demo Mode){RESET}")
    print("Executing Python Hadoop Streaming mappers and reducers directly.\n")
    
    # Run Job 1: Content Type and Release Year
    run_pipeline("Content Type Distribution", MAPPER_PY, REDUCER_PY, DATASET_PATH)
    
    # Run Job 2: Genre Frequency
    run_pipeline("Top Genres Distribution", MAPPER_GENRE_PY, REDUCER_GENRE_PY, DATASET_PATH, limit=10)
