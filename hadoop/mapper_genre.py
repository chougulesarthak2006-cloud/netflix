#!/usr/bin/env python3
"""
mapper_genre.py
---------------
Hadoop Streaming Mapper for Netflix Genre & Category Distribution.
Task: Explodes comma-separated listed_in categories into individual genre keys.

Input: Comma-separated CSV lines from STDIN.
Output: Tab-delimited key-value pairs: <Genre>\t1
"""

import sys
import csv

def main():
    reader = csv.reader(sys.stdin)
    for row in reader:
        if not row or len(row) < 11:
            continue
        if row[0].strip().lower() == "show_id":
            continue
            
        genres_str = row[10].strip() if len(row) > 10 else ""
        if genres_str:
            genres = [g.strip() for g in genres_str.split(",") if g.strip()]
            for genre in genres:
                print(f"{genre}\t1")

if __name__ == "__main__":
    main()
