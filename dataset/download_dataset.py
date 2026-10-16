#!/usr/bin/env python3
"""
download_dataset.py
-------------------
Utility script to download or verify the Netflix Movies & TV Shows dataset
for the Hadoop/Hive Big Data Project.

Usage:
    python download_dataset.py
"""

import os
import sys
import urllib.request
import csv

DATASET_URL = "https://raw.githubusercontent.com/prasertcbs/basic-dataset/master/netflix_titles.csv"
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_FILE = os.path.join(CURRENT_DIR, "netflix_titles.csv")
SAMPLE_FILE = os.path.join(CURRENT_DIR, "sample_netflix_titles.csv")

def download_dataset():
    print(f"[*] Checking dataset at: {OUTPUT_FILE}")
    if os.path.exists(OUTPUT_FILE) and os.path.getsize(OUTPUT_FILE) > 1000000:
        print("[+] Full dataset already exists locally. Verifying rows...")
    else:
        print(f"[*] Downloading dataset from {DATASET_URL}...")
        try:
            urllib.request.urlretrieve(DATASET_URL, OUTPUT_FILE)
            print("[+] Download complete!")
        except Exception as e:
            print(f"[-] Error downloading dataset: {e}", file=sys.stderr)
            sys.exit(1)

    # Validate dataset
    total_rows = 0
    with open(OUTPUT_FILE, 'r', encoding='utf-8', errors='replace') as f:
        reader = csv.reader(f)
        header = next(reader)
        sample_rows = []
        for i, row in enumerate(reader):
            total_rows += 1
            if i < 25:
                sample_rows.append(row)

    print(f"[+] Total Records Verified: {total_rows} titles.")
    print(f"[+] Columns ({len(header)}): {', '.join(header)}")

    # Create a 25-row sample file for lightweight testing
    with open(SAMPLE_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(sample_rows)
    print(f"[+] Sample dataset (25 rows) saved at: {SAMPLE_FILE}")

if __name__ == "__main__":
    download_dataset()
