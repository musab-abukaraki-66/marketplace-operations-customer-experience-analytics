# Data quality report

**Source:** Olist Brazilian E-Commerce Public Dataset (8 CSVs, downloaded 2026-10-14 from Kaggle, `olistbr/brazilian-ecommerce`). Raw files are not committed.
**Run:** `python -m src.pipeline` on the real data. Raw output: [`reports/data_quality_results.csv`](../reports/data_quality_results.csv). Checks: [`sql/05_data_quality/checks.sql`](../sql/05_data_quality/checks.sql). No check was loosened or changed for this run.

**Result: all 13 blocking checks passed (0 failing rows); the 7 informational checks are listed below with their counts.**

## Blocking checks (pipeline fails if any has rows)
| Check | Failing rows |
|---|---|
| Duplicate `order_id` in orders | 0 |
| Duplicate `customer_id` in customers | 0 |
| Duplicate (`order_id`, `order_item_id`) in items | 0 |
| `fact_orders` row count differs from `clean_orders` | 0 |
| Items with no matching order | 0 |
| Payments with no matching order | 0 |
| Orders with no matching customer | 0 |
| Negative or NULL item price | 0 |
| Product value: fact vs. raw items, reconciliation difference | 0 |
| Freight value: fact vs. raw items, reconciliation difference | 0 |
| Payment value: fact vs. raw payments, reconciliation difference | 0 |
| Review score outside 1-5 | 0 |
| Unparseable purchase timestamp | 0 |

## Informational checks (documented, do not fail the run)
| Check | Count | Effect on analysis |
|---|---|---|
| Delivered orders with no delivery timestamp | 8 | Not delivery-eligible; never counted as on time. Eligible orders: 96,470 of 96,478 delivered. |
| Delivery timestamp before purchase timestamp | 0 | No exclusions needed. |
| Orders without any item row | 775 | 603 `unavailable`, 164 `canceled`, 8 other (5 `created`, 2 `invoiced`, 1 `shipped`). Excluded from product sales value and from the AOV denominator. |
| Orders without a review | 768 | Excluded from review KPIs (reviews are voluntary). |
| Extra review rows (rows minus distinct orders) | 551 | One review per order is kept: the most recently created (rule in `docs/methodology.md`). |
| Products whose category has no English translation | 13 | Keep the Portuguese category name. |
| Orders with an unexpected status value | 0 | - |

## Other observations from the real data (not covered by a check)
- **Coverage.** Purchases run 2016-09-04 to 2018-10-17. Sep-Dec 2016 hold 4, 324, 0 (no November) and 1 orders, and Sep-Oct 2018 hold 16 and 4 (all statuses). Only Jan 2017 - Aug 2018 are full months, so trend and growth comparisons use that window. The monthly chart shows only months with at least 500 orders.
- **Orders per customer.** 99,441 `customer_id` values map to 96,096 distinct `customer_unique_id` values, so `customer_unique_id` is required for repeat-purchase analysis.
- **Fan-out is real.** 4,446 extra payment rows and 551 extra review rows exist. A naive orders x items x payments join inflates product value by 4.5% on this data (see the notebook, section 6); the order-grain model avoids this.
- **Payment vs. price + freight.** 260 of 98,665 orders with both values differ by more than 0.05 (vouchers, installment interest or rounding are possible explanations; not investigated).
- **Currency** is not stated in the dataset. Values are reported as recorded.

## Limits of this report
The checks cover keys, referential integrity, ranges and reconciliation to the raw files. They do not verify that the data reflects real-world events (the dataset is a public, anonymised extract), and no completeness check against an external source is possible.
