-- Uptime Summary by Host
-- Calculates total checks, up/down counts, and uptime percentage per target

SELECT
    target,
    COUNT(*) AS total_checks,
    SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) AS up_count,
    SUM(CASE WHEN status = 'down' THEN 1 ELSE 0 END) AS down_count,
    ROUND(100.0 * SUM(CASE WHEN status = 'up' THEN 1 ELSE 0 END) / COUNT(*), 2) AS uptime_pct
FROM ping_log
GROUP BY target
ORDER BY uptime_pct ASC;