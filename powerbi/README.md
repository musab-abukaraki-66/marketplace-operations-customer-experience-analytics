# Power BI

**Status: no `.pbix` exists.** Power BI Desktop is not available in the authoring environment (Linux, cloud), so no report file was built or validated and no screenshots exist. Provided instead: model design, relationships and DAX, ready to implement.

Steps: run the pipeline; in Power BI Desktop use Get Data → Text/CSV for `data/processed/fact_orders.csv`, `fact_order_items.csv`, `dim_date.csv`; set relationships per `model_relationships.md`; add measures from `measures_dax.md`; build the four pages (Executive Overview, Sales & Product Mix, Delivery & Customer Experience, Customer & Seller Intelligence) as outlined in `../docs/requirements_traceability.md`.
