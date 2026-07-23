# Latency Monitor

### TCP Network Latency Collection & Analysis Framework

**Author:** Akshat Arora

---

# 1. Overview

This project was developed to collect and analyze TCP connection latency over long durations. The original motivation was to study network latency characteristics relevant to algorithmic trading and eventually High Frequency / Medium Frequency Trading (HFT/MFT).

Instead of measuring latency for a few seconds using utilities like `ping` or `tcping`, the objective is to continuously collect latency measurements throughout an entire trading session (typically 09:00–16:00), store them in a structured format, and perform offline statistical analysis.

The project is intentionally divided into two phases:

* **Data Collection**
* **Data Analysis**

Keeping these phases independent allows raw data to remain unchanged while analysis techniques evolve over time.

---

# 2. Objectives

The project aims to:

* Collect TCP connection latency periodically.
* Monitor multiple hosts simultaneously.
* Store measurements in CSV format.
* Analyze latency trends.
* Compute useful statistics.
* Visualize network behaviour.
* Build a reusable monitoring framework that can later be adapted to exchange connectivity.

---

# 3. Project Structure

```
latency-monitor/

├── collector.sh
├── analyze.sh
├── latency-collector.service
├── targets.conf

├── logs/
│   ├── 2026-07-14.csv
│   └── ...

├── report/
│   ├── latency.png
│   ├── histogram.png
│   ├── boxplot.png
│   ├── jitter.png
│   └── statistics.csv

├── tools/
│   ├── latency.py
│   ├── analyze.py
│   ├── compare.py
│   └── plot.py

└── env/
```

---

# 4. Workflow

The project follows a simple pipeline.

```
Targets
      │
      ▼

collector.sh
      │
      ▼

CSV Log Files
      │
      ▼

Python Analysis
      │
      ▼

Statistics
Plots
Reports
```

---

# 5. Data Collection

The collector periodically performs TCP connection attempts using **Nmap's `nping`**.

Each sample is appended to a CSV log.

Typical fields include

```
timestamp
target
host
port
RTT
packet loss
status
```

Each day's measurements are stored separately.

Example

```
logs/

2026-07-14.csv

2026-07-15.csv
```

This makes long-term monitoring significantly easier.

---

# 6. Configuration

Targets are separated from the collector.

Example:

```
Google,google.com,443
Cloudflare,1.1.1.1,443
Quad9,9.9.9.9,443
NSE,nseindia.com,443
```

The collector never needs modification when adding or removing endpoints.

---

# 7. Why TCP Instead of ICMP?

Traditional `ping` measures ICMP latency.

However, trading systems communicate over TCP.

Measuring TCP handshake latency provides a metric that is much closer to actual application behaviour.

---

# 8. Data Analysis

Python is used for analysis because it provides powerful numerical and visualization libraries.

Libraries:

* pandas
* numpy
* matplotlib

The analysis currently generates:

* Latency vs Time
* Histogram
* Box Plot
* Jitter Plot
* Statistical Summary

---

# 9. Statistical Metrics

The project computes:

* Sample Count
* Minimum RTT
* Maximum RTT
* Average RTT
* Median RTT
* Standard Deviation
* P95 Latency
* P99 Latency
* Average Jitter
* Maximum Jitter

These metrics are considerably more informative than a simple average.

---

# 10. Why Jitter?

Average latency alone can hide instability.

Example:

```
15
15
15
15
60
15
15
```

Average latency appears reasonable while a trading strategy would still experience a noticeable delay.

Jitter captures these fluctuations.

---

# 11. Daily Reports

The analysis stage produces

```
report/

latency.png

histogram.png

boxplot.png

jitter.png

statistics.csv
```

This separates raw data from derived information.

---

# 12. Systemd Integration

Instead of using `nohup`, the collector was integrated into systemd.

Advantages:

* Automatic startup
* Automatic restart on failures
* Background execution
* Service management
* Standard Linux deployment model

Useful commands:

```
systemctl start latency-collector

systemctl stop latency-collector

systemctl restart latency-collector

systemctl status latency-collector

journalctl -u latency-collector
```

---

# 13. Lessons Learned

## systemd does not execute shell expansions

The following does **not** work:

```
collector_$(date +%F).log
```

inside

```
StandardOutput=
```

Systemd reads the value literally.

---

## Service files use absolute paths

Incorrect paths prevent services from starting.

The following must always match the actual installation.

```
WorkingDirectory=

ExecStart=
```

---

## daemon-reload

Whenever a service file changes:

```
sudo systemctl daemon-reload
```

must be executed before restarting the service.

---

## Understanding systemctl status

Useful fields include:

```
Loaded
Active
Main PID
Invocation ID
```

These are usually sufficient to identify startup failures.

---

## Reading journal logs

The most useful debugging command became

```
journalctl -xeu latency-collector
```

rather than simply reading terminal output.

---

## TCP vs Exchange Connectivity

A major discovery during development:

The following worked

```
nseindia.com:443
```

because it is publicly reachable.

However,

```
172.19.x.x
```

addresses from the NSE documentation are private RFC1918 addresses.

These require:

* leased line
* VPN
* exchange connectivity

and therefore cannot be reached from a home Internet connection.

---

# 14. Design Decisions

Several architectural decisions were intentionally made.

## Separate configuration from code

Targets live in

```
targets.conf
```

instead of being hardcoded.

---

## Separate collection from analysis

The collector never computes statistics.

It simply records measurements.

Analysis is entirely offline.

---

## Immutable raw data

CSV files are treated as raw observations.

Reports are regenerated whenever needed.

---

## Daily log files

Using one file per day avoids extremely large CSV files while making archival straightforward.

---

# 15. Future Improvements

Possible future enhancements include:

* Parallel TCP probing
* Interactive Plotly dashboard
* HTML report generation
* Multi-day comparison
* Automatic anomaly detection
* Percentile trend analysis
* Geographic comparison
* Exchange connectivity analysis
* Broker latency comparison
* Grafana/InfluxDB integration
* Prometheus exporter
* Real-time dashboard
* Packet capture correlation
* Traceroute correlation
* DNS lookup latency measurement
* TLS handshake timing
* Automatic report generation at market close

---

# 16. Key Takeaways

This project evolved from a simple latency measurement script into a modular monitoring framework.

It introduced practical experience with:

* Bash scripting
* TCP latency measurement
* CSV-based data logging
* Python data analysis
* Statistical characterization
* Data visualization
* Linux service management
* systemd
* Long-running background services
* Log management
* Network troubleshooting

Although originally motivated by trading applications, the overall architecture is general enough to monitor any TCP-based service over extended periods.

The separation between collection and analysis provides a clean foundation for future experimentation and makes the framework easy to extend without modifying the data acquisition process.

