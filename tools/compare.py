#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt

files = sys.argv[1:]

plt.figure(figsize=(15,6))

for file in files:

    df = pd.read_csv(file)

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["rtt_ms"] = pd.to_numeric(df["rtt_ms"], errors="coerce")

    google = df[df.target=="Google"]

    plt.plot(
        google.timestamp,
        google.rtt_ms,
        label=file
    )

plt.legend()

plt.grid(True)

plt.tight_layout()

plt.show()
