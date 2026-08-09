<<<<<<< HEAD
"""
audit_report.py
-----------------
Reads the ping_log data collected by uptime_monitor.py, runs SQL queries
to calculate uptime %, average latency, and detect anomalies, prints a
summary report, exports a CSV, and generates an uptime trend chart.
"""

import sqlite3
import csv
import json
from datetime import datetime
import matplotlib.pyplot as plt


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def get_connection(db_file):
    return sqlite3.connect(db_file)


def uptime_summary(conn):
    query = """
        SELECT
            target,
            COUNT(*) AS total_checks,
            SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) AS up_count,
            SUM(CASE WHEN status = 'down' THEN 1 ELSE 0 END) AS down_count,
            ROUND(100.0 * SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) / COUNT(*), 2) AS uptime_pct,
            ROUND(AVG(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS avg_latency_ms,
            ROUND(MAX(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS max_latency_ms
        FROM ping_log
        GROUP BY target
        ORDER BY uptime_pct ASC
    """
    return conn.execute(query).fetchall()


def downtime_events(conn):
    query = """
        SELECT target, timestamp
        FROM ping_log
        WHERE status = 'down'
        ORDER BY timestamp DESC
    """
    return conn.execute(query).fetchall()


def high_latency_events(conn, threshold_ms):
    query = """
        SELECT target, timestamp, response_time_ms
        FROM ping_log
        WHERE status = 'up' AND response_time_ms > ?
        ORDER BY response_time_ms DESC
    """
    return conn.execute(query, (threshold_ms,)).fetchall()


def latency_over_time(conn, target):
    query = """
        SELECT timestamp, response_time_ms
        FROM ping_log
        WHERE target = ? AND status = 'up'
        ORDER BY timestamp ASC
    """
    return conn.execute(query, (target,)).fetchall()


def export_summary_csv(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "target", "total_checks", "up_count", "down_count",
            "uptime_pct", "avg_latency_ms", "max_latency_ms"
        ])
        writer.writerows(rows)


def generate_chart(conn, targets, chart_path):
    plt.figure(figsize=(10, 6))
    has_data = False
    for target in targets:
        rows = latency_over_time(conn, target)
        if not rows:
            continue
        latencies = [r[1] for r in rows]
        plt.plot(range(len(latencies)), latencies, marker="o", markersize=3, label=target)
        has_data = True

    if has_data:
        plt.title("Response Time Trend by Target")
        plt.xlabel("Check Number (chronological)")
        plt.ylabel("Response Time (ms)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(chart_path)
        print(f"✅ Chart saved to '{chart_path}'")
    else:
        print("No latency data available to chart.")
    plt.close()


def print_report():
    config = load_config()
    db_file = config["db_file"]
    threshold = config["high_latency_threshold_ms"]
    targets = config["targets"]

    conn = get_connection(db_file)

    print("=" * 60)
    print(f"NETWORK UPTIME & DATA QUALITY AUDIT REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    summary_rows = uptime_summary(conn)
    if not summary_rows:
        print("\nNo data found. Run uptime_monitor.py first to collect logs.")
        conn.close()
        return

    print("\n--- UPTIME SUMMARY BY TARGET ---")
    print(f"{'Target':<15}{'Checks':<8}{'Up':<6}{'Down':<6}{'Uptime%':<10}{'AvgMs':<8}{'MaxMs':<8}")
    for row in summary_rows:
        target, total, up, down, pct, avg_ms, max_ms = row
        print(f"{target:<15}{total:<8}{up:<6}{down:<6}{pct:<10}{avg_ms or '-':<8}{max_ms or '-':<8}")

    downs = downtime_events(conn)
    print(f"\n--- DOWNTIME EVENTS ({len(downs)} total) ---")
    if downs:
        for target, ts in downs[:10]:
            print(f"  [DOWN] {target} at {ts}")
    else:
        print("  None detected.")

    highs = high_latency_events(conn, threshold)
    print(f"\n--- HIGH LATENCY ANOMALIES (> {threshold}ms) — {len(highs)} total ---")
    if highs:
        for target, ts, rtt in highs[:10]:
            print(f"  [SLOW] {target} at {ts} — {rtt} ms")
    else:
        print("  None detected.")

    export_summary_csv(summary_rows, "uptime_report.csv")
    print(f"\n✅ Summary exported to 'uptime_report.csv'")

    generate_chart(conn, targets, "uptime_chart.png")

    conn.close()


if __name__ == "__main__":
=======
"""
audit_report.py
-----------------
Reads the ping_log data collected by uptime_monitor.py, runs SQL queries
to calculate uptime %, average latency, and detect anomalies, prints a
summary report, exports a CSV, and generates an uptime trend chart.
"""

import sqlite3
import csv
import json
from datetime import datetime
import matplotlib.pyplot as plt


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def get_connection(db_file):
    return sqlite3.connect(db_file)


def uptime_summary(conn):
    query = """
        SELECT
            target,
            COUNT(*) AS total_checks,
            SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) AS up_count,
            SUM(CASE WHEN status = 'down' THEN 1 ELSE 0 END) AS down_count,
            ROUND(100.0 * SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) / COUNT(*), 2) AS uptime_pct,
            ROUND(AVG(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS avg_latency_ms,
            ROUND(MAX(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS max_latency_ms
        FROM ping_log
        GROUP BY target
        ORDER BY uptime_pct ASC
    """
    return conn.execute(query).fetchall()


def downtime_events(conn):
    query = """
        SELECT target, timestamp
        FROM ping_log
        WHERE status = 'down'
        ORDER BY timestamp DESC
    """
    return conn.execute(query).fetchall()


def high_latency_events(conn, threshold_ms):
    query = """
        SELECT target, timestamp, response_time_ms
        FROM ping_log
        WHERE status = 'up' AND response_time_ms > ?
        ORDER BY response_time_ms DESC
    """
    return conn.execute(query, (threshold_ms,)).fetchall()


def latency_over_time(conn, target):
    query = """
        SELECT timestamp, response_time_ms
        FROM ping_log
        WHERE target = ? AND status = 'up'
        ORDER BY timestamp ASC
    """
    return conn.execute(query, (target,)).fetchall()


def export_summary_csv(rows, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "target", "total_checks", "up_count", "down_count",
            "uptime_pct", "avg_latency_ms", "max_latency_ms"
        ])
        writer.writerows(rows)


def generate_chart(conn, targets, chart_path):
    plt.figure(figsize=(10, 6))
    has_data = False
    for target in targets:
        rows = latency_over_time(conn, target)
        if not rows:
            continue
        latencies = [r[1] for r in rows]
        plt.plot(range(len(latencies)), latencies, marker="o", markersize=3, label=target)
        has_data = True

    if has_data:
        plt.title("Response Time Trend by Target")
        plt.xlabel("Check Number (chronological)")
        plt.ylabel("Response Time (ms)")
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(chart_path)
        print(f"✅ Chart saved to '{chart_path}'")
    else:
        print("No latency data available to chart.")
    plt.close()


def print_report():
    config = load_config()
    db_file = config["db_file"]
    threshold = config["high_latency_threshold_ms"]
    targets = config["targets"]

    conn = get_connection(db_file)

    print("=" * 60)
    print(f"NETWORK UPTIME & DATA QUALITY AUDIT REPORT")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    summary_rows = uptime_summary(conn)
    if not summary_rows:
        print("\nNo data found. Run uptime_monitor.py first to collect logs.")
        conn.close()
        return

    print("\n--- UPTIME SUMMARY BY TARGET ---")
    print(f"{'Target':<15}{'Checks':<8}{'Up':<6}{'Down':<6}{'Uptime%':<10}{'AvgMs':<8}{'MaxMs':<8}")
    for row in summary_rows:
        target, total, up, down, pct, avg_ms, max_ms = row
        print(f"{target:<15}{total:<8}{up:<6}{down:<6}{pct:<10}{avg_ms or '-':<8}{max_ms or '-':<8}")

    downs = downtime_events(conn)
    print(f"\n--- DOWNTIME EVENTS ({len(downs)} total) ---")
    if downs:
        for target, ts in downs[:10]:
            print(f"  [DOWN] {target} at {ts}")
    else:
        print("  None detected.")

    highs = high_latency_events(conn, threshold)
    print(f"\n--- HIGH LATENCY ANOMALIES (> {threshold}ms) — {len(highs)} total ---")
    if highs:
        for target, ts, rtt in highs[:10]:
            print(f"  [SLOW] {target} at {ts} — {rtt} ms")
    else:
        print("  None detected.")

    export_summary_csv(summary_rows, "uptime_report.csv")
    print(f"\n✅ Summary exported to 'uptime_report.csv'")

    generate_chart(conn, targets, "uptime_chart.png")

    conn.close()


if __name__ == "__main__":
>>>>>>> a5464d5e63d1991adf80a5953b87006c34430dbc
    print_report()