#!/usr/bin/env python3
"""
reducer_genre.py
----------------
Hadoop Streaming Reducer for Netflix Genre & Category Distribution.
Task: Aggregates counts per genre.

Input: Tab-delimited <Genre>\t1 lines (sorted).
Output: <Genre>\t<TotalCount>
"""

import sys

def main():
    current_genre = None
    current_count = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split("\t")
        if len(parts) != 2:
            continue
            
        genre, count_str = parts[0], parts[1]
        try:
            count = int(count_str)
        except ValueError:
            continue
            
        if current_genre == genre:
            current_count += count
        else:
            if current_genre is not None:
                print(f"{current_genre}\t{current_count}")
            current_genre = genre
            current_count = count
            
    if current_genre is not None:
        print(f"{current_genre}\t{current_count}")

if __name__ == "__main__":
    main()
