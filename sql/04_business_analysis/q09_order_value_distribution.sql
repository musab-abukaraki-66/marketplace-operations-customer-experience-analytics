-- BQ9: How is order value distributed? (product sales value = SUM(item price) per order)
-- Population: active orders (not canceled/unavailable) with >= 1 item. Grain: order -> value band.
-- Bands are fixed so results are comparable across runs; freight excluded.
WITH banded AS (
  SELECT order_id, product_value,
         CASE WHEN product_value <  50  THEN '1: < 50'
              WHEN product_value < 100  THEN '2: 50-99.99'
              WHEN product_value < 200  THEN '3: 100-199.99'
              WHEN product_value < 500  THEN '4: 200-499.99'
              ELSE                           '5: 500+' END AS value_band
  FROM fact_orders
  WHERE order_status NOT IN ('canceled', 'unavailable') AND product_value IS NOT NULL)
SELECT value_band,
       COUNT(*)                                   AS orders,
       COUNT(*) * 1.0 / SUM(COUNT(*)) OVER ()     AS order_share,
       SUM(product_value)                         AS product_sales_value,
       SUM(product_value) / SUM(SUM(product_value)) OVER () AS value_share
FROM banded GROUP BY 1 ORDER BY 1;
