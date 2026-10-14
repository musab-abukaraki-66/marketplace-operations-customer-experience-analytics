# Model relationships

| From (many) | To (one) | Column | Direction | Active |
|---|---|---|---|---|
| fact_orders | dim_date | purchase_date → date_key | single | yes |
| fact_order_items | fact_orders | order_id | single (facts filter from orders) | yes |

No many-to-many relationships. Payments and reviews are already at order grain inside `fact_orders`. Mark `dim_date` as the date table. `customer_state` is an attribute of `fact_orders`.
