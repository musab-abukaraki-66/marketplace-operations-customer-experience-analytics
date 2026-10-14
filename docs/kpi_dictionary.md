# KPI dictionary

General rules: analysis is at the grains stated below; items/payments/reviews are pre-aggregated to order grain before joining (`sql/03_analytical_marts/01_marts.sql`); NULLs are never silently treated as "on time" or zero.
"Product sales value" is the sum of item `price`; it is **not** accounting revenue, profit or net sales. Freight is reported separately. Payment value is reported separately and may differ from price+freight (vouchers, installment interest).

| KPI | Definition / formula | Denominator & exclusions | Grain | SQL | DAX (see `powerbi/measures_dax.md`) | Limitations |
|---|---|---|---|---|---|---|
| Total Orders | count of order_id | all statuses unless stated | order | q03 | `Total Orders` | includes canceled |
| Orders (active) | orders with status not in canceled/unavailable | – | order | q01, q06 | `Active Orders` | unavailable ≠ canceled semantically |
| Canceled Order Rate | canceled / all orders | all orders | order | q03 | `Canceled Rate` | |
| Product Sales Value | SUM(price) | active orders | item→order | q01, q02 | `Product Sales Value` | not revenue |
| Freight Value | SUM(freight_value) | as above | item→order | q01 | `Freight Value` | |
| Average Order Value | Product Sales Value / active orders having ≥1 item | orders without items excluded from denominator | order | q01 | `AOV` | excludes freight |
| Monthly Order Growth | (orders_m − orders_m-1)/orders_m-1 | consecutive months | month | derived from q01 | `MoM Order Growth` | early/late partial months distort |
| Delivery-eligible orders | status=delivered, delivered_ts & estimated_ts present, delivered_ts ≥ purchase_ts | – | order | `fact_orders.delivery_eligible` | `Eligible Deliveries` | records violating rules are excluded and counted in QA |
| Avg Delivery Days | AVG(delivered_ts − purchase_ts) in days | eligible orders | order | q04 | `Avg Delivery Days` | purchase→customer |
| Late Delivery Rate | late / eligible, late = delivered_ts > estimated_ts | eligible | order | q04 | `Late Rate` | |
| On-Time Rate | 1 − Late Rate (same denominator) | eligible | order | derived | `On-Time Rate` | missing timestamps NOT counted on time |
| Avg Review Score | AVG(review_score) | orders with a review; one review per order (latest) | order | q05 | `Avg Review Score` | voluntary reviews → selection bias |
| Low-Score Rate | score ≤ 2 / reviewed orders | reviewed | order | q05 | `Low Score Rate` | |
| Repeat-Customer Rate | customers with >1 active order / distinct customer_unique_id | active orders | customer_unique_id | q06 | `Repeat Rate` | only within observed window |
| Category Contribution | category value / total value | active orders | category | q02 | `Category Share` | category of each item; untranslated categories keep Portuguese name |
| Payment Distribution | orders by payment_type | – | payment record | q08 | `Orders by Payment Type` | orders with multiple types counted in each |
