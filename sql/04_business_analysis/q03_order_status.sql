-- BQ3: What proportion of orders are delivered, canceled, unavailable or otherwise?
SELECT order_status, COUNT(*) AS orders, COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS share
FROM fact_orders GROUP BY 1 ORDER BY orders DESC;
