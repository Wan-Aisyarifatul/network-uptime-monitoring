-- Anomaly Detection
-- Returns downtime events and high-latency events with timestamps
-- Note: replace the 150 threshold below to match your config.json's
-- "high_latency_threshold_ms" value if you change it

-- Downtime events
SELECT
    target,
    timestamp,
    'DOWNTIME' AS event_type
FROM ping_log
WHERE status = 'down'

UNION ALL

-- High-latency events
SELECT
    target,
    timestamp,
    'HIGH_LATENCY' AS event_type
FROM ping_log
WHERE status = 'up' AND response_time_ms > 150

ORDER BY timestamp DESC;