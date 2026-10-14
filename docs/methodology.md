# Methodology

1. **Validate** source files/columns (`src/ingestion/validate_sources.py`).
2. **Stage** CSVs as text, **type** with `TRY_CAST` (no row dropped) — `sql/01_staging`, `sql/02_transformations`.
3. **Aggregate before joining**: items, payments, reviews → order grain (`sql/03_analytical_marts`). `fact_orders` must keep exactly one row per `order_id`.
4. **Review rule**: where an order has several reviews, the one with the latest `review_creation_date` (tie: highest `review_id`) is used.
5. **Dominant category/seller per order**: the highest-priced item (used only for order-level segmenting; category/seller KPIs use `fact_order_items`).
6. **Quality gate**: `sql/05_data_quality/checks.sql`; `error` checks stop the pipeline, `info` checks are recorded in `reports/data_quality_results.csv` and drive the data quality report.
7. **Analyse** with the numbered queries in `sql/04_business_analysis`; outputs in `reports/`.
8. **Minimum volume**: segment/seller rankings require ≥ 30 eligible orders.
Comparisons are descriptive; association is not causation. No statistical significance testing is claimed.
