#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt

import os
from pathlib import Path

# Get the directory of the current script
script_dir = Path(__file__).resolve().parent

# Build the path to the log file (adjust the number of parents if needed)
file_path = script_dir.parent / 'logs' / '2026-07-14.csv'

FILE = file_path

df = pd.read_csv(FILE)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["rtt_ms"] = pd.to_numeric(df["rtt_ms"], errors="coerce")

plt.figure(figsize=(15,6))

for target, group in df.groupby("target"):
    plt.plot(
        group["timestamp"],
        group["rtt_ms"],
        label=target,
        linewidth=1
    )

plt.xlabel("Time")
plt.ylabel("TCP RTT (ms)")
plt.title("Network Latency")
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig("latency.png", dpi=300)

#plt.show()
