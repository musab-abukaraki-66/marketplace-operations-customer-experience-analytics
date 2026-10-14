-- Marts. Every fact is pre-aggregated to ORDER grain before being joined, so
-- items, payments and reviews cannot fan out monetary measures.

-- Item values per order (grain: order_id)
CREATE OR REPLACE TABLE mart_order_items_agg AS
SELECT order_id,
       COUNT(*)            AS item_count,
       SUM(price)          AS product_value,
       SUM(freight_value)  AS freight_value
FROM clean_order_items
GROUP BY order_id;

-- Recorded payments per order (grain: order_id)
CREATE OR REPLACE TABLE mart_order_payments_agg AS
SELECT order_id,
       SUM(payment_value)                              AS payment_value,
       COUNT(*)                                        AS payment_records,
       MAX(payment_installments)                       AS max_installments,
       arg_max(payment_type, payment_value)            AS main_payment_type
FROM clean_payments
GROUP BY order_id;

-- One review per order: the most recently created review (ties: highest review_id).
-- Rule documented in docs/methodology.md.
CREATE OR REPLACE TABLE mart_order_review AS
SELECT order_id, review_score
FROM (
  SELECT order_id, review_score,
         ROW_NUMBER() OVER (PARTITION BY order_id
                            ORDER BY review_created_ts DESC NULLS LAST, review_id DESC) AS rn
  FROM clean_reviews
) WHERE rn = 1;

-- Dominant category per order = category of the highest-priced item (grain: order_id)
CREATE OR REPLACE TABLE mart_order_category AS
SELECT order_id, category, seller_id
FROM (
  SELECT i.order_id, p.category, i.seller_id,
         ROW_NUMBER() OVER (PARTITION BY i.order_id ORDER BY i.price DESC, i.order_item_id) AS rn
  FROM clean_order_items i
  LEFT JOIN clean_products p USING (product_id)
) WHERE rn = 1;

-- Central order fact (grain: order_id; row count must equal clean_orders)
CREATE OR REPLACE TABLE fact_orders AS
SELECT o.order_id,
       c.customer_unique_id, c.customer_state,
       o.order_status,
       o.purchase_ts, CAST(o.purchase_ts AS DATE) AS purchase_date,
       DATE_TRUNC('month', o.purchase_ts)         AS purchase_month,
       o.delivered_ts, o.estimated_ts,
       a.item_count, a.product_value, a.freight_value,
       p.payment_value, p.main_payment_type, p.max_installments,
       r.review_score,
       oc.category AS dominant_category,
       oc.seller_id AS dominant_seller_id,
       -- Delivery KPIs only defined for delivered orders with both timestamps
       (o.order_status = 'delivered' AND o.delivered_ts IS NOT NULL AND o.estimated_ts IS NOT NULL
        AND o.delivered_ts >= o.purchase_ts)                                   AS delivery_eligible,
       DATE_DIFF('second', o.purchase_ts, o.delivered_ts) / 86400.0            AS delivery_days,
       CASE WHEN o.order_status = 'delivered' AND o.delivered_ts IS NOT NULL AND o.estimated_ts IS NOT NULL
                 AND o.delivered_ts >= o.purchase_ts
            THEN o.delivered_ts > o.estimated_ts END                           AS is_late
FROM clean_orders o
LEFT JOIN clean_customers c USING (customer_id)
LEFT JOIN mart_order_items_agg a USING (order_id)
LEFT JOIN mart_order_payments_agg p USING (order_id)
LEFT JOIN mart_order_review r USING (order_id)
LEFT JOIN mart_order_category oc USING (order_id);

-- Item-level fact for category / seller analysis (grain: order_id + order_item_id)
CREATE OR REPLACE TABLE fact_order_items AS
SELECT i.order_id, i.order_item_id, i.seller_id, i.product_id,
       p.category, i.price, i.freight_value,
       f.purchase_month, f.order_status, f.review_score, f.is_late, f.delivery_eligible,
       s.seller_state
FROM clean_order_items i
JOIN fact_orders f USING (order_id)
LEFT JOIN clean_products p USING (product_id)
LEFT JOIN clean_sellers s USING (seller_id);

CREATE OR REPLACE TABLE dim_date AS
SELECT CAST(d AS DATE) AS date_key, YEAR(d) AS year, MONTH(d) AS month,
       DATE_TRUNC('month', d) AS month_start, STRFTIME(d, '%Y-%m') AS year_month
FROM generate_series(
  (SELECT CAST(MIN(purchase_ts) AS DATE) FROM clean_orders),
  (SELECT CAST(MAX(purchase_ts) AS DATE) FROM clean_orders),
  INTERVAL 1 DAY) t(d);
