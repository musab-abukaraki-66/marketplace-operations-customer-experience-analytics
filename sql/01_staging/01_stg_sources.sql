-- Staging: load raw Olist CSVs with explicit column types. No cleaning here.
-- {{DATA_DIR}} is substituted by src/pipeline.py.
CREATE OR REPLACE TABLE stg_customers AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_customers_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_orders AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_orders_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_order_items AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_order_items_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_payments AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_order_payments_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_reviews AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_order_reviews_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_products AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_products_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_sellers AS
SELECT * FROM read_csv('{{DATA_DIR}}/olist_sellers_dataset.csv', header = true, all_varchar = true);

CREATE OR REPLACE TABLE stg_category_translation AS
SELECT * FROM read_csv('{{DATA_DIR}}/product_category_name_translation.csv', header = true, all_varchar = true);
