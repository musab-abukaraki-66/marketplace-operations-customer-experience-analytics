-- BQ5: Association between late delivery and review score (association, not causation).
SELECT CASE WHEN is_late THEN 'late' ELSE 'on_time' END AS delivery_outcome,
       COUNT(*)                                          AS orders_with_review,
       AVG(review_score)                                 AS avg_review_score,
       AVG(CASE WHEN review_score <= 2 THEN 1.0 ELSE 0.0 END) AS low_score_rate
FROM fact_orders
WHERE delivery_eligible AND review_score IS NOT NULL
GROUP BY 1 ORDER BY 1;
