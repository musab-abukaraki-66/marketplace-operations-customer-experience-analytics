-- BQ9 (by category): order-value distribution per dominant category
-- (category of the highest-priced item in the order; see mart_order_category).
-- Population: active orders with >= 1 item. Categories need >= 100 orders.
SELECT dominant_category AS category,
       COUNT(*)                                        AS orders,
       QUANTILE_CONT(product_value, 0.25)              AS p25_order_value,
       QUANTILE_CONT(product_value, 0.50)              AS median_order_value,
       QUANTILE_CONT(product_value, 0.75)              AS p75_order_value,
       AVG(product_value)                              AS avg_order_value
FROM fact_orders
WHERE order_status NOT IN ('canceled', 'unavailable') AND product_value IS NOT NULL
GROUP BY 1
HAVING COUNT(*) >= 100
ORDER BY median_order_value DESC;
