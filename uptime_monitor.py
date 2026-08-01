"""
uptime_monitor.py
------------------
Pings a list of target hosts at regular intervals (configured in config.json),
measures response time, logs results into a SQLite database, and writes
alerts to a log file whenever a host goes down.
"""

import sqlite3
import time
import json
from datetime import datetime
from ping3 import ping


def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)


def init_db(db_file):
    """Create the database table if it doesn't exist yet."""
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ping_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            target TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            status TEXT NOT NULL,
            response_time_ms REAL
        )
    """)
    conn.commit()
    conn.close()


def log_ping_result(db_file, target, status, response_time_ms):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO ping_log (target, timestamp, status, response_time_ms) VALUES (?, ?, ?, ?)",
        (target, datetime.now().isoformat(timespec="seconds"), status, response_time_ms)
    )
    conn.commit()
    conn.close()


def write_alert(alert_log_file, message):
    """Append an alert line to the alert log file with a timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(alert_log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")


def check_target(target):
    """Ping a single target and return (status, response_time_ms)."""
    try:
        result = ping(target, timeout=2)
        if result is None or result is False:
            return "down", None
        response_time_ms = round(result * 1000, 2)
        return "up", response_time_ms
    except Exception as e:
        print(f"  ! Error pinging {target}: {e}")
        return "down", None


def run_monitor():
    config = load_config()
    targets = config["targets"]
    interval = config["check_interval_seconds"]
    db_file = config["db_file"]
    alert_log_file = config["alert_log_file"]
    latency_threshold = config["high_latency_threshold_ms"]

    init_db(db_file)
    print(f"Monitoring started. Config loaded from 'config.json'.")
    print(f"Targets: {targets}")
    print(f"Logging data to '{db_file}', alerts to '{alert_log_file}'. Press Ctrl+C to stop.\n")

    try:
        while True:
            print(f"--- Check at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            for target in targets:
                status, rtt = check_target(target)
                log_ping_result(db_file, target, status, rtt)

                if status == "up":
                    print(f"  [UP]   {target:<15} {rtt} ms")
                    if rtt > latency_threshold:
                        msg = f"HIGH LATENCY: {target} responded in {rtt} ms (threshold: {latency_threshold} ms)"
                        write_alert(alert_log_file, msg)
                        print(f"  [ALERT] {msg}")
                else:
                    print(f"  [DOWN] {target:<15} no response")
                    write_alert(alert_log_file, f"HOST DOWN: {target} did not respond")

            print(f"Sleeping {interval}s...\n")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user.")


if __name__ == "__main__":
    run_monitor()