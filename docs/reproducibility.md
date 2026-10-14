# Reproducibility

```bash
python -m venv .venv && source .venv/bin/activate
make setup            # pip install -r requirements.txt
make test             # tests on synthetic fixture (no real data needed)
# download real data to data/raw/ (see data/raw/README.md), then:
make pipeline         # writes reports/*.csv, reports/charts/*.png, data/processed/*.csv
```
Environment used for the verified test run: Python 3.13, DuckDB 1.5, pandas 3.0, pytest. CI uses Python 3.12.
