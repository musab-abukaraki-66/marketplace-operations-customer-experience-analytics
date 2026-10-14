# Data quality report

**Status: REAL-DATA RUN NOT EXECUTED.** The Olist CSVs could not be downloaded in the authoring environment (Kaggle was blocked by network policy), so no real-data quality results exist and none are reported here.

What exists: the checks are implemented in `sql/05_data_quality/checks.sql` and are tested on the synthetic fixture (`tests/test_pipeline.py`). After a real run, `reports/data_quality_results.csv` holds the actual counts; paste/summarise them in this file.

Checks: primary-key uniqueness, foreign-key orphans, negative/NULL prices, review score range, unparseable purchase timestamps, monetary reconciliation (fact vs. raw) — all fail the pipeline. Informational: delivered without delivery timestamp, delivery before purchase, orders without items/reviews, duplicate reviews per order, untranslated categories, unexpected statuses.
