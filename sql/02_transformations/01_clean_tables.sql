-- Type normalization. Rows are never dropped here; only typed with TRY_CAST so
-- invalid values surface as NULL and are counted by the quality checks.
CREATE OR REPLACE TABLE clean_customers AS
SELECT customer_id, customer_unique_id,
       customer_zip_code_prefix, customer_city, customer_state
FROM stg_customers;

CREATE OR REPLACE TABLE clean_orders AS
SELECT order_id, customer_id, order_status,
       TRY_CAST(order_purchase_timestamp      AS TIMESTAMP) AS purchase_ts,
       TRY_CAST(order_approved_at             AS TIMESTAMP) AS approved_ts,
       TRY_CAST(order_delivered_carrier_date  AS TIMESTAMP) AS carrier_ts,
       TRY_CAST(order_delivered_customer_date AS TIMESTAMP) AS delivered_ts,
       TRY_CAST(order_estimated_delivery_date AS TIMESTAMP) AS estimated_ts
FROM stg_orders;

CREATE OR REPLACE TABLE clean_order_items AS
SELECT order_id, TRY_CAST(order_item_id AS INTEGER) AS order_item_id,
       product_id, seller_id,
       TRY_CAST(price AS DOUBLE)         AS price,
       TRY_CAST(freight_value AS DOUBLE) AS freight_value
FROM stg_order_items;

CREATE OR REPLACE TABLE clean_payments AS
SELECT order_id, TRY_CAST(payment_sequential AS INTEGER) AS payment_sequential,
       payment_type,
       TRY_CAST(payment_installments AS INTEGER) AS payment_installments,
       TRY_CAST(payment_value AS DOUBLE)         AS payment_value
FROM stg_payments;

CREATE OR REPLACE TABLE clean_reviews AS
SELECT review_id, order_id,
       TRY_CAST(review_score AS INTEGER)               AS review_score,
       TRY_CAST(review_creation_date AS TIMESTAMP)     AS review_created_ts,
       TRY_CAST(review_answer_timestamp AS TIMESTAMP)  AS review_answered_ts
FROM stg_reviews;

CREATE OR REPLACE TABLE clean_products AS
SELECT p.product_id,
       COALESCE(t.product_category_name_english, p.product_category_name, 'unknown') AS category,
       (p.product_category_name IS NOT NULL AND t.product_category_name_english IS NULL) AS category_untranslated
FROM stg_products p
LEFT JOIN stg_category_translation t USING (product_category_name);

CREATE OR REPLACE TABLE clean_sellers AS
SELECT seller_id, seller_city, seller_state FROM stg_sellers;
