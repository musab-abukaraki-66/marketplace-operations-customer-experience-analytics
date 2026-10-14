-- BQ1: How do order volumes and product sales value change over time?
-- Grain: month. Product sales value = SUM(item price), freight reported separately.
SELECT purchase_month,
       COUNT(*)                                   AS orders,
       SUM(product_value)                         AS product_sales_value,
       SUM(freight_value)                         AS freight_value,
       SUM(product_value) / NULLIF(COUNT(*) FILTER (WHERE product_value IS NOT NULL), 0) AS avg_order_value
FROM fact_orders
WHERE order_status NOT IN ('canceled', 'unavailable')
GROUP BY 1 ORDER BY 1;
