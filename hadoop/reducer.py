#!/usr/bin/env python3
"""
reducer.py
----------
Hadoop Streaming Reducer for Netflix Dataset Analysis.
Task: Aggregates key-value counts from mapper output after Hadoop Shuffle & Sort.

Input: Tab-delimited key-value pairs from STDIN (sorted by key).
Output: Aggregated counts:
        <MetricCategory>\t<Key>\t<TotalCount>
"""

import sys

def main():
    current_category = None
    current_key = None
    current_count = 0
    
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
            
        parts = line.split("\t")
        if len(parts) == 3:
            category, key, count_str = parts[0], parts[1], parts[2]
        elif len(parts) == 2:
            category = "GENERAL"
            key, count_str = parts[0], parts[1]
        else:
            continue
            
        try:
            count = int(count_str)
        except ValueError:
            continue
            
        composite_key = f"{category}::{key}"
        
        # If key changes, flush previous aggregate
        if current_key == composite_key:
            current_count += count
        else:
            if current_key is not None:
                cat, k = current_key.split("::", 1)
                print(f"{cat}\t{k}\t{current_count}")
            current_key = composite_key
            current_count = count
            
    # Output the last key
    if current_key is not None:
        cat, k = current_key.split("::", 1)
        print(f"{cat}\t{k}\t{current_count}")

if __name__ == "__main__":
    main()
