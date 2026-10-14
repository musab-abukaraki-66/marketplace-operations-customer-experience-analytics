"""Run each business-analysis query and export CSV + (optionally) charts."""
import logging
from pathlib import Path

from src.config import SQL_DIR

log = logging.getLogger(__name__)


def run_queries(con, out_dir: Path) -> dict:
    out_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    for f in sorted((SQL_DIR / "04_business_analysis").glob("q*.sql")):
        df = con.execute(f.read_text()).df()
        df.to_csv(out_dir / f"{f.stem}.csv", index=False)
        results[f.stem] = df
        log.info("%s -> %d rows", f.stem, len(df))
    return results


def make_charts(results: dict, chart_dir: Path) -> None:
    from src.analysis.charts import make_all
    make_all(results, chart_dir)
