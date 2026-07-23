#!/usr/bin/env python3

import pandas as pd
import os
from pathlib import Path

# Get the directory of the current script
script_dir = Path(__file__).resolve().parent

# Build the path to the log file (adjust the number of parents if needed)
file_path = script_dir.parent / 'logs' / '2026-07-14.csv'

#FILE = "../logs/2026-07-14.csv"
FILE = file_path


df = pd.read_csv(FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["rtt_ms"] = pd.to_numeric(df["rtt_ms"], errors="coerce")

print()

for target, group in df.groupby("target"):

    rtt = group["rtt_ms"].dropna()

    if len(rtt) == 0:
        continue

    print("=" * 60)
    print(target)

    print(f"Samples : {len(rtt)}")
    print(f"Minimum : {rtt.min():.3f} ms")
    print(f"Average : {rtt.mean():.3f} ms")
    print(f"Median  : {rtt.median():.3f} ms")
    print(f"Maximum : {rtt.max():.3f} ms")
    print(f"Std Dev : {rtt.std():.3f} ms")

    print(f"P95     : {rtt.quantile(0.95):.3f} ms")
    print(f"P99     : {rtt.quantile(0.99):.3f} ms")
