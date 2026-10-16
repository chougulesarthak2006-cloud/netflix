#!/usr/bin/env python3
"""
mapper.py
---------
Hadoop Streaming Mapper for Netflix Dataset Analysis.
Task: Content Type & Release Year Distribution (Movie vs TV Show by Year).

Input: Comma-separated CSV lines from STDIN.
Output: Tab-delimited key-value pairs to STDOUT:
        <Type>\t1
        <Type_ReleaseYear>\t1
"""

import sys
import csv

def main():
    # Process standard input line by line (Hadoop streaming standard)
    reader = csv.reader(sys.stdin)
    
    for row in reader:
        # Skip empty lines or header
        if not row or len(row) < 8:
            continue
        if row[0].strip().lower() == "show_id":
            continue
            
        content_type = row[1].strip() if len(row) > 1 else ""
        release_year = row[7].strip() if len(row) > 7 else ""
        
        if content_type:
            # Emit content type count
            print(f"TYPE\t{content_type}\t1")
            
            # Emit content type by release year
            if release_year and release_year.isdigit():
                print(f"YEAR\t{release_year}\t1")
                print(f"TYPE_YEAR\t{content_type}_{release_year}\t1")

if __name__ == "__main__":
    main()
