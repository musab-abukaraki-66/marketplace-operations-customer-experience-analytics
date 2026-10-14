"""End-to-end pipeline: validate sources -> build models -> quality checks -> analysis outputs.

Usage: python -m src.pipeline [--data-dir DIR] [--out-dir DIR] [--no-charts]
"""
import argparse
import logging
import sys
from pathlib import Path

import duckdb

from src import config
from src.analysis.run_analysis import make_charts, run_queries
from src.ingestion.validate_sources import SourceDataError, validate_sources
from src.quality.checks import DataQualityError, assert_checks, run_checks
from src.transformation.run_sql import build_models

log = logging.getLogger("pipeline")


def run(data_dir: Path, out_dir: Path, charts: bool = True, db_path: str = ":memory:") -> dict:
    validate_sources(data_dir)
    con = duckdb.connect(db_path)
    build_models(con, data_dir)
    qa = run_checks(con)
    out_dir.mkdir(parents=True, exist_ok=True)
    qa.to_csv(out_dir / "data_quality_results.csv", index=False)
    assert_checks(qa)
    results = run_queries(con, out_dir)
    # Star-schema extracts for Power BI
    pbi = config.DATA_PROCESSED if out_dir == config.REPORTS else out_dir / "processed"
    pbi.mkdir(parents=True, exist_ok=True)
    for t in ["fact_orders", "fact_order_items", "dim_date"]:
        con.execute(f"COPY {t} TO '{(pbi / (t + '.csv')).as_posix()}' (HEADER, DELIMITER ',')")
    if charts:
        make_charts(results, out_dir / "charts")
    return {"quality": qa, "results": results}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", type=Path, default=config.DATA_RAW)
    ap.add_argument("--out-dir", type=Path, default=config.REPORTS)
    ap.add_argument("--no-charts", action="store_true")
    a = ap.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    try:
        run(a.data_dir, a.out_dir, charts=not a.no_charts)
    except (SourceDataError, DataQualityError) as e:
        log.error("%s", e)
        return 1
    log.info("pipeline complete")
    return 0


if __name__ == "__main__":
    sys.exit(main())
