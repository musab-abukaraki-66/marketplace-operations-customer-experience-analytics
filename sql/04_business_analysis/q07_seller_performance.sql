-- BQ7: Seller delivery/review outcomes with a minimum-volume safeguard (>= 30 eligible orders).
-- Seller measured on item rows; orders with several sellers contribute to each seller.
SELECT seller_id, seller_state,
       COUNT(DISTINCT order_id)                        AS orders,
       AVG(review_score)                               AS avg_review_score,
       AVG(CASE WHEN is_late THEN 1.0 ELSE 0.0 END)    AS late_rate
FROM fact_order_items
WHERE delivery_eligible
GROUP BY 1, 2
HAVING COUNT(DISTINCT order_id) >= 30
ORDER BY late_rate DESC, orders DESC;
