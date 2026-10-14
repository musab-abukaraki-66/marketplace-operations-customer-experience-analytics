# Reproducibility

```bash
python -m venv .venv && source .venv/bin/activate
make setup            # pip install -r requirements.txt
make test             # tests on synthetic fixture (no real data needed)
# download real data to data/raw/ (see data/raw/README.md), then:
make pipeline         # writes reports/*.csv, reports/charts/*.png, data/processed/*.csv
```
The notebook `notebooks/01_exploratory_data_analysis.ipynb` reads `data/raw/` through the same SQL models; to re-run it: `pip install jupyter` (or `nbformat nbclient ipykernel`), then execute it from the repo root or `notebooks/`.

Real-data run: Olist data downloaded 2026-10-14 from Kaggle (`olistbr/brazilian-ecommerce`); all outputs in `reports/` and `docs/` come from that run.
Environment used for the verified test run: Python 3.13, DuckDB 1.5, pandas 3.0, pytest. CI uses Python 3.12.
