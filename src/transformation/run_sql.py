"""Execute the numbered SQL layers in order against a DuckDB connection."""
import logging
from pathlib import Path

import duckdb

from src.config import SQL_DIR

log = logging.getLogger(__name__)
BUILD_LAYERS = ["01_staging", "02_transformations", "03_analytical_marts"]


def run_file(con, path: Path, data_dir: Path) -> None:
    sql = path.read_text().replace("{{DATA_DIR}}", Path(data_dir).resolve().as_posix())
    con.execute(sql)


def build_models(con: duckdb.DuckDBPyConnection, data_dir: Path) -> None:
    for layer in BUILD_LAYERS:
        for f in sorted((SQL_DIR / layer).glob("*.sql")):
            log.info("running %s", f.relative_to(SQL_DIR))
            run_file(con, f, data_dir)
