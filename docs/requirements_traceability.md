# Requirements traceability

Business Question → KPI → Source → Grain → Method → Dashboard visual → Finding → Recommendation.
Findings and recommendations are from the real-data run (see [`findings_and_recommendations.md`](findings_and_recommendations.md)). "Dashboard visual" is the *planned* Power BI visual: no `.pbix` has been built (see `powerbi/README.md`).

| # | Business question | KPI | Source tables | Grain | Method | Dashboard visual (planned) | Finding / Rec. |
|---|---|---|---|---|---|---|---|
| BQ1 | How do orders and sales evolve? | Orders, Product Sales Value, AOV | orders, items | month | `q01_monthly_trend.sql` | P1/P2 line chart | F1 |
| BQ2 | Which categories contribute most? | Category share | items, products, translation | category | `q02_category_contribution.sql` | P2 bar | F2 |
| BQ2b | Which categories grew or lost share? | Growth rate, share change (Jan-Aug 2018 vs 2017) | items, products | category | `q13_category_growth.sql` | P2 bar | F9, R6 |
| BQ3 | Order outcomes? | Status share, Canceled rate | orders | order | `q03_order_status.sql` | P1 status bar | Data quality report; status mix in `reports/q03_order_status.csv` (97.0% delivered, 0.6% canceled) |
| BQ4 | Delivery time and lateness by region? | Avg delivery days, Late rate | orders, customers | order (eligible) | `q04_delivery_performance.sql` | P3 | F3, R1 |
| BQ5 | Delay vs review score? | Avg score, Low-score rate | orders, reviews | order | `q05_reviews_vs_delay.sql` | P3 | F4, R3 |
| BQ6 | Repeat customers? | Repeat-customer rate | orders, customers | customer_unique_id | `q06_repeat_customers.sql` | P4 | F5, R4 |
| BQ7 | Sellers needing attention? | Seller late rate / score (min 30 orders) | items, orders, reviews | seller | `q07_seller_performance.sql` | P4 | F6, R2 |
| BQ8 | Payment behaviour? | Payment-type share, installments | payments | payment record | `q08_payments.sql` | P2 | F8 |
| BQ8b | Payment patterns by order-value band? | Payment-type share, instalment share per band | orders, payments | order -> value band | `q12_payments_by_order_value_band.sql` | P2 stacked bar | F8, R5 |
| BQ9 | How is order value distributed? | Order-value bands, value share | orders, items | order -> value band | `q09_order_value_distribution.sql` | P2 column | F7 |
| BQ9b | ... by category and by geography? | Order-value quartiles | orders, items, customers | category / state | `q10_order_value_by_category.sql`, `q11_order_value_by_state.sql` | P2 / P3 | F7 |

All twelve questions have SQL and a real-data result. Remaining gap: the Power BI visuals are specified in `powerbi/` but not built.
