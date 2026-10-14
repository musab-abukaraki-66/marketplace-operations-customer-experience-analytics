"""Project paths and settings. Everything is relative to the repo root."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = Path(os.environ.get("OLIST_DATA_DIR", ROOT / "data" / "raw"))
DATA_PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports"
SQL_DIR = ROOT / "sql"

REQUIRED_FILES = {
    "olist_customers_dataset.csv": ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"],
    "olist_orders_dataset.csv": ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at",
                                 "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"],
    "olist_order_items_dataset.csv": ["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"],
    "olist_order_payments_dataset.csv": ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"],
    "olist_order_reviews_dataset.csv": ["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message",
                                        "review_creation_date", "review_answer_timestamp"],
    "olist_products_dataset.csv": ["product_id", "product_category_name"],
    "olist_sellers_dataset.csv": ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"],
    "product_category_name_translation.csv": ["product_category_name", "product_category_name_english"],
}
