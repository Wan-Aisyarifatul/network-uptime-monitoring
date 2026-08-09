-- Latency Analysis by Host
-- Calculates average, minimum, and maximum response time per target
-- and ranks hosts from slowest to fastest average latency

SELECT
    target,
    ROUND(AVG(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS avg_latency_ms,
    ROUND(MIN(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS min_latency_ms,
    ROUND(MAX(CASE WHEN status = 'up' THEN response_time_ms END), 2) AS max_latency_ms
FROM ping_log
WHERE status = 'up'
GROUP BY target
ORDER BY avg_latency_ms DESC;