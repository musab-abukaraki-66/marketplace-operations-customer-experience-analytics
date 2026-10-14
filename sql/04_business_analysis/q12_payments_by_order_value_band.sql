-- BQ8 (by order value): payment behaviour per order-value band (bands as in q09).
-- Population: active orders with >= 1 item and >= 1 payment record.
-- main_payment_type = type with the largest recorded payment value in the order.
WITH banded AS (
  SELECT order_id, product_value, main_payment_type, max_installments,
         CASE WHEN product_value <  50  THEN '1: < 50'
              WHEN product_value < 100  THEN '2: 50-99.99'
              WHEN product_value < 200  THEN '3: 100-199.99'
              WHEN product_value < 500  THEN '4: 200-499.99'
              ELSE                           '5: 500+' END AS value_band
  FROM fact_orders
  WHERE order_status NOT IN ('canceled', 'unavailable')
    AND product_value IS NOT NULL AND main_payment_type IS NOT NULL)
SELECT value_band,
       COUNT(*)                                                        AS orders,
       AVG(CASE WHEN main_payment_type = 'credit_card' THEN 1.0 ELSE 0.0 END) AS credit_card_share,
       AVG(CASE WHEN main_payment_type = 'boleto'      THEN 1.0 ELSE 0.0 END) AS boleto_share,
       AVG(CASE WHEN main_payment_type = 'voucher'     THEN 1.0 ELSE 0.0 END) AS voucher_share,
       AVG(CASE WHEN main_payment_type = 'debit_card'  THEN 1.0 ELSE 0.0 END) AS debit_card_share,
       AVG(max_installments)                                           AS avg_max_installments,
       AVG(CASE WHEN max_installments > 1 THEN 1.0 ELSE 0.0 END)       AS installment_share
FROM banded GROUP BY 1 ORDER BY 1;
