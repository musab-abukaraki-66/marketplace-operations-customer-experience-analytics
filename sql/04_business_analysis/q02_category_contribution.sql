-- BQ2: Which categories contribute most to product sales value and order activity?
-- Grain: category (from item-level fact). Orders counted DISTINCT per category.
SELECT category,
       COUNT(DISTINCT order_id) AS orders,
       SUM(price)               AS product_sales_value,
       SUM(price) / SUM(SUM(price)) OVER () AS value_share
FROM fact_order_items
WHERE order_status NOT IN ('canceled', 'unavailable')
GROUP BY 1 ORDER BY product_sales_value DESC;
