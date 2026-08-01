# Network Uptime & Data Quality Monitor

A Python + SQL tool that monitors network host uptime in real time, logs the results to a database, detects anomalies, sends alerts, and visualizes latency trends.

## Overview
This project combines **network monitoring** (ping-based uptime checks, latency measurement), **data analysis** (SQL aggregation, anomaly detection), and **automated alerting/visualization** — a lightweight simulation of the kind of monitoring tooling used in NOC/IT support environments.

## How It Works
1. **`config.json`** — central configuration file: target hosts, check interval, database/log file names, and the high-latency threshold. Change monitoring behavior here without touching the code.
2. **`uptime_monitor.py`** — pings each configured host at regular intervals, logs status (up/down) and response time into a SQLite database (`network_monitor.db`), and writes an alert line to `alerts.log` whenever a host goes down or responds above the latency threshold.
3. **`audit_report.py`** — runs SQL queries against the logged data to calculate uptime %, average/max latency, downtime events, and high-latency anomalies. Prints a console summary, exports `uptime_report.csv`, and generates `uptime_chart.png` — a line chart of response time trends per host.

## Tech Stack
- **Python** — `ping3` (ICMP ping), `sqlite3` (database), `json` (config), `matplotlib` (charting), `csv` (export)
- **SQL** — aggregate queries (`GROUP BY`, `CASE WHEN`, `AVG`, conditional filtering) for uptime calculation and anomaly detection

## How to Run
\`\`\`bash
pip install -r requirements.txt

python uptime_monitor.py    # let it run (e.g. 15-30 min), then Ctrl+C to stop
python audit_report.py      # generates report, CSV, and chart
\`\`\`

Outputs after running:
- `network_monitor.db` — raw ping log data
- `alerts.log` — timestamped alerts for downtime / high latency
- `uptime_report.csv` — summary table (uptime %, latency stats per host)
- `uptime_chart.png` — response time trend chart

## Configuration
Edit `config.json` to change monitored hosts, check frequency, or the latency alert threshold — no code changes needed:
\`\`\`json
{
    "targets": ["8.8.8.8", "1.1.1.1", "google.com", "github.com"],
    "check_interval_seconds": 30,
    "db_file": "network_monitor.db",
    "alert_log_file": "alerts.log",
    "high_latency_threshold_ms": 150
}
\`\`\`

## Author
Wan Aisyarifatul Nor Binti Wan Aziz