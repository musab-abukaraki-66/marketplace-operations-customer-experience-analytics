# Requirements traceability

Business Question → KPI → Source → Grain → Method → Dashboard visual → Finding → Recommendation.
**Findings/recommendations are `PENDING REAL-DATA RUN`**: the real dataset could not be downloaded in the authoring environment (see README, "Project status").

| # | Business question | KPI | Source tables | Grain | Method | Dashboard visual | Finding / Rec. |
|---|---|---|---|---|---|---|---|
| BQ1 | How do orders and sales evolve? | Orders, Product Sales Value, AOV | orders, items | month | `q01_monthly_trend.sql` | P1/P2 line chart | PENDING |
| BQ2 | Which categories contribute most? | Category share | items, products, translation | category | `q02_category_contribution.sql` | P2 bar | PENDING |
| BQ3 | Order outcomes? | Status share, Canceled rate | orders | order | `q03_order_status.sql` | P1 status bar | PENDING |
| BQ4 | Delivery time and lateness by region? | Avg delivery days, Late rate | orders, customers | order (eligible) | `q04_delivery_performance.sql` | P3 | PENDING |
| BQ5 | Delay vs review score? | Avg score, Low-score rate | orders, reviews | order | `q05_reviews_vs_delay.sql` | P3 | PENDING |
| BQ6 | Repeat customers? | Repeat-customer rate | orders, customers | customer_unique_id | `q06_repeat_customers.sql` | P4 | PENDING |
| BQ7 | Sellers needing attention? | Seller late rate / score (min 30 orders) | items, orders, reviews | seller | `q07_seller_performance.sql` | P4 | PENDING |
| BQ8 | Payment behaviour? | Payment-type share, installments | payments | payment record | `q08_payments.sql` | P2 | PENDING |

Not yet implemented as SQL: order-value distribution by category/geography, payment patterns by order-value band, category growth/decline. They remain open requirements.
