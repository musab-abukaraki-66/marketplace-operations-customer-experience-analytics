-- BQ9 (by geography): order-value distribution per customer state.
-- Population: active orders with >= 1 item. States need >= 100 orders.
SELECT customer_state,
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
