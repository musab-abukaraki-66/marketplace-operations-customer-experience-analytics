-- BQ4: Delivery duration and late-delivery rate by customer state.
-- Denominator: delivered orders with both timestamps and delivered >= purchase (delivery_eligible).
-- Orders missing timestamps are NOT counted as on time.
SELECT customer_state,
       COUNT(*)                                 AS eligible_orders,
       AVG(delivery_days)                       AS avg_delivery_days,
       AVG(CASE WHEN is_late THEN 1.0 ELSE 0.0 END) AS late_rate
FROM fact_orders
WHERE delivery_eligible
GROUP BY 1
HAVING COUNT(*) >= 30   -- minimum-volume safeguard
ORDER BY late_rate DESC;
