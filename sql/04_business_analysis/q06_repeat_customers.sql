-- BQ6: Share of distinct customers (customer_unique_id) with >1 order in the period.
-- Excludes canceled/unavailable orders.
WITH per_customer AS (
  SELECT customer_unique_id, COUNT(DISTINCT order_id) AS orders
  FROM fact_orders
  WHERE order_status NOT IN ('canceled', 'unavailable') AND customer_unique_id IS NOT NULL
  GROUP BY 1)
SELECT COUNT(*)                                   AS customers,
       COUNT(*) FILTER (WHERE orders > 1)         AS repeat_customers,
       COUNT(*) FILTER (WHERE orders > 1) * 1.0 / COUNT(*) AS repeat_rate
FROM per_customer;
