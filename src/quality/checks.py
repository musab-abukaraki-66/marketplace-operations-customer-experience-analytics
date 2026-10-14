"""Run sql/05_data_quality/checks.sql; fail on any 'error' check with failing rows."""
import logging

import pandas as pd

from src.config import SQL_DIR

log = logging.getLogger(__name__)


class DataQualityError(RuntimeError):
    pass


def run_checks(con) -> pd.DataFrame:
    df = con.execute((SQL_DIR / "05_data_quality" / "checks.sql").read_text()).df()
    df["failing_rows"] = df["failing_rows"].astype(int)
    df["passed"] = (df["severity"] != "error") | (df["failing_rows"] == 0)
    return df


def assert_checks(df: pd.DataFrame) -> None:
    bad = df[~df["passed"]]
    if len(bad):
        raise DataQualityError("Data quality checks failed:\n" + bad.to_string(index=False))
