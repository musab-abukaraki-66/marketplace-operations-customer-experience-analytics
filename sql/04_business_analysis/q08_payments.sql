-- BQ8: Payment type and installment behaviour (grain: payment record).
SELECT payment_type,
       COUNT(DISTINCT order_id)    AS orders,
       SUM(payment_value)          AS payment_value,
       AVG(payment_installments)   AS avg_installments
FROM clean_payments GROUP BY 1 ORDER BY orders DESC;
