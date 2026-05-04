#!/usr/bin/env python3
"""Standalone log decoder for keylogger output."""
import sys
from pathlib import Path

def decode_log(filepath):
    path = Path(filepath)
    if not path.exists():
        print(f"File not found: {filepath}")
        return
    print(path.read_text(encoding='utf-8', errors='ignore'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        decode_log(sys.argv[1])
    else:
        print("Usage: python decoder.py <logfile>")