# Data model

```mermaid
erDiagram
  dim_date ||--o{ fact_orders : purchase_date
  fact_orders ||--o{ fact_order_items : order_id
  fact_orders {
    string order_id PK "one row per order"
    string customer_unique_id
    string customer_state
    string order_status
    date purchase_date
    double product_value
    double freight_value
    double payment_value
    int review_score
    bool delivery_eligible
    bool is_late
  }
  fact_order_items {
    string order_id FK
    int order_item_id
    string seller_id
    string category
    double price
    double freight_value
  }
```
Grains: `fact_orders` = order; `fact_order_items` = order item. Payments and reviews are aggregated into `fact_orders`; raw payment records are available in `clean_payments` for the payment-type analysis (q08).
