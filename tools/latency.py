#!/usr/bin/env python3

import argparse
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# ------------------------------------------------------------
# Arguments
# ------------------------------------------------------------

parser = argparse.ArgumentParser(description="Latency Analyzer")

parser.add_argument(
    "--input",
    required=True,
    help="CSV file"
)

parser.add_argument(
    "--target",
    action="append",
    help="Target(s) to analyze"
)

parser.add_argument(
    "--from-time",
    dest="from_time",
    help="HH:MM"
)

parser.add_argument(
    "--to-time",
    dest="to_time",
    help="HH:MM"
)

parser.add_argument(
    "--output",
    default="report"
)

args = parser.parse_args()

os.makedirs(args.output, exist_ok=True)


# ------------------------------------------------------------
# Read CSV
# ------------------------------------------------------------

df = pd.read_csv(args.input)

df["timestamp"] = pd.to_datetime(df["timestamp"])
df["rtt_ms"] = pd.to_numeric(df["rtt_ms"], errors="coerce")

df = df[df["status"] == "OK"]

# ------------------------------------------------------------
# Target filter
# ------------------------------------------------------------

if args.target:
    df = df[df["target"].isin(args.target)]

# ------------------------------------------------------------
# Time filter
# ------------------------------------------------------------

if args.from_time:

    start = datetime.strptime(args.from_time, "%H:%M").time()

    df = df[df["timestamp"].dt.time >= start]

if args.to_time:

    end = datetime.strptime(args.to_time, "%H:%M").time()

    df = df[df["timestamp"].dt.time <= end]

if df.empty:
    print("No data after filtering.")
    exit(1)

# ------------------------------------------------------------
# Statistics
# ------------------------------------------------------------

print("\n========== Statistics ==========\n")

stats = []

for target, group in df.groupby("target"):

    rtt = group["rtt_ms"].dropna()

    jitter = rtt.diff().abs()

    s = {
        "Target": target,
        "Samples": len(rtt),
        "Min": rtt.min(),
        "Mean": rtt.mean(),
        "Median": rtt.median(),
        "Max": rtt.max(),
        "StdDev": rtt.std(),
        "P95": rtt.quantile(.95),
        "P99": rtt.quantile(.99),
        "AvgJitter": jitter.mean(),
        "MaxJitter": jitter.max()
    }

    stats.append(s)

    print("=" * 50)
    print(target)

    for k, v in s.items():
        if k in ("Target", "Samples"):
            print(f"{k:12}: {v}")
        else:
            print(f"{k:12}: {v:.3f} ms")

stats_df = pd.DataFrame(stats)

stats_df.to_csv(
    os.path.join(args.output, "statistics.csv"),
    index=False
)

# ------------------------------------------------------------
# Latency plot
# ------------------------------------------------------------

plt.figure(figsize=(15,6))

for target, group in df.groupby("target"):

    plt.plot(
        group["timestamp"],
        group["rtt_ms"],
        label=target
    )

plt.title("Latency vs Time")
plt.xlabel("Time")
plt.ylabel("Latency (ms)")
plt.grid(True)
plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(args.output, "latency.png"),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Histogram
# ------------------------------------------------------------

plt.figure(figsize=(10,6))

for target, group in df.groupby("target"):

    plt.hist(
        group["rtt_ms"],
        bins=40,
        alpha=.5,
        label=target
    )

plt.grid(True)
plt.legend()

plt.xlabel("Latency (ms)")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig(
    os.path.join(args.output, "histogram.png"),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Box plot
# ------------------------------------------------------------

plt.figure(figsize=(8,6))

groups = []

labels = []

for target, group in df.groupby("target"):

    labels.append(target)

    groups.append(group["rtt_ms"])

plt.boxplot(groups, tick_labels=labels)

plt.ylabel("Latency (ms)")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(args.output, "boxplot.png"),
    dpi=300
)

plt.close()

# ------------------------------------------------------------
# Jitter
# ------------------------------------------------------------

plt.figure(figsize=(15,6))

for target, group in df.groupby("target"):

    jitter = group["rtt_ms"].diff().abs()

    plt.plot(
        group["timestamp"],
        jitter,
        label=target
    )

plt.xlabel("Time")
plt.ylabel("Jitter (ms)")
plt.title("Jitter vs Time")

plt.grid(True)

plt.legend()

plt.tight_layout()

plt.savefig(
    os.path.join(args.output, "jitter.png"),
    dpi=300
)

plt.close()

print("\nReports written to:", args.output)


