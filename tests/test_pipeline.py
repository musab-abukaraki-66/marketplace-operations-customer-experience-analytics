"""Tests run on the SYNTHETIC fixture (tests/fixtures), not the real Olist dataset."""
import shutil
from pathlib import Path

import duckdb
import pytest

from src.ingestion.validate_sources import SourceDataError, validate_sources
from src.pipeline import main, run
from src.quality.checks import DataQualityError, assert_checks, run_checks
from src.transformation.run_sql import build_models

FIX = Path(__file__).parent / "fixtures"


@pytest.fixture(scope="module")
def con():
    c = duckdb.connect(":memory:")
    build_models(c, FIX)
    return c


def test_missing_source_is_clear_error(tmp_path):
    with pytest.raises(SourceDataError, match="missing file"):
        validate_sources(tmp_path)
    assert main(["--data-dir", str(tmp_path), "--out-dir", str(tmp_path / "o")]) == 1


def test_missing_column_detected(tmp_path):
    for f in FIX.glob("*.csv"):
        shutil.copy(f, tmp_path)
    (tmp_path / "olist_orders_dataset.csv").write_text("order_id,customer_id\no1,c1\n")
    with pytest.raises(SourceDataError, match="missing columns"):
        validate_sources(tmp_path)


def test_orders_grain_preserved(con):
    n_clean = con.execute("SELECT COUNT(*) FROM clean_orders").fetchone()[0]
    n_fact = con.execute("SELECT COUNT(*) FROM fact_orders").fetchone()[0]
    n_dist = con.execute("SELECT COUNT(DISTINCT order_id) FROM fact_orders").fetchone()[0]
    assert n_clean == n_fact == n_dist


def test_fixture_exercises_fanout_cases(con):
    assert con.execute("SELECT COUNT(*) FROM clean_order_items").fetchone()[0] > con.execute(
        "SELECT COUNT(DISTINCT order_id) FROM clean_order_items").fetchone()[0]
    assert con.execute("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM clean_payments").fetchone()[0] > 0
    assert con.execute("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM clean_reviews").fetchone()[0] > 0


@pytest.mark.parametrize("fact_sql,raw_sql", [
    ("SELECT SUM(product_value) FROM fact_orders", "SELECT SUM(price) FROM clean_order_items"),
    ("SELECT SUM(freight_value) FROM fact_orders", "SELECT SUM(freight_value) FROM clean_order_items"),
    ("SELECT SUM(payment_value) FROM fact_orders", "SELECT SUM(payment_value) FROM clean_payments"),
    ("SELECT SUM(price) FROM fact_order_items", "SELECT SUM(price) FROM clean_order_items"),
])
def test_monetary_reconciliation(con, fact_sql, raw_sql):
    assert con.execute(fact_sql).fetchone()[0] == pytest.approx(con.execute(raw_sql).fetchone()[0], abs=0.01)


def test_naive_join_would_inflate(con):
    """Documents WHY pre-aggregation is required."""
    naive = con.execute("""SELECT SUM(i.price) FROM clean_order_items i
                           JOIN clean_payments p USING (order_id)""").fetchone()[0]
    true = con.execute("SELECT SUM(price) FROM clean_order_items").fetchone()[0]
    assert naive > true


def test_missing_delivery_ts_not_counted_on_time(con):
    row = con.execute("""SELECT delivery_eligible, is_late FROM fact_orders WHERE order_id='o3'""").fetchone()
    assert row == (False, None)
    total_flagged = con.execute("SELECT COUNT(*) FROM fact_orders WHERE is_late IS NOT NULL").fetchone()[0]
    assert total_flagged == con.execute("SELECT COUNT(*) FROM fact_orders WHERE delivery_eligible").fetchone()[0]


def test_one_review_per_order_latest_wins(con):
    assert con.execute("SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM mart_order_review").fetchone()[0] == 0
    # o0 has r0b (later creation date) as duplicate; r0 does not exist because i % 7 == 0 -> only r0b
    assert con.execute("SELECT COUNT(*) FROM mart_order_review WHERE order_id='o0'").fetchone()[0] == 1


def test_untranslated_category_flagged(con):
    assert con.execute("SELECT COUNT(*) FROM clean_products WHERE category_untranslated").fetchone()[0] > 0


def test_repeat_rate_formula(con):
    r = con.execute((Path(__file__).parents[1] / "sql/04_business_analysis/q06_repeat_customers.sql").read_text()).fetchone()
    customers, repeat, rate = r
    assert 0 < repeat < customers
    assert rate == pytest.approx(repeat / customers)


def test_quality_checks_pass_on_fixture(con):
    qa = run_checks(con)
    assert_checks(qa)
    assert qa.loc[qa.check_name == "info_delivered_missing_delivery_ts", "failing_rows"].iloc[0] >= 1


def test_quality_check_fails_visibly(con):
    c = duckdb.connect(":memory:")
    build_models(c, FIX)
    c.execute("INSERT INTO clean_order_items VALUES ('o0', 99, 'p0', 's0', 10.0, 1.0)")
    with pytest.raises(DataQualityError):
        assert_checks(run_checks(c))


def test_full_pipeline_outputs(tmp_path):
    res = run(FIX, tmp_path, charts=True)
    for q in res["results"]:
        assert (tmp_path / f"{q}.csv").exists()
    assert {"orders", "product_sales_value"} <= set(res["results"]["q01_monthly_trend"].columns)
    assert (tmp_path / "processed" / "fact_orders.csv").exists()
    assert (tmp_path / "charts" / "monthly_orders.png").exists()


def _q(con, name):
    return con.execute((Path(__file__).parents[1] / f"sql/04_business_analysis/{name}.sql").read_text()).df()


def test_order_value_bands_reconcile(con):
    bands = _q(con, "q09_order_value_distribution")
    exp = con.execute("""SELECT COUNT(*), SUM(product_value) FROM fact_orders
                         WHERE order_status NOT IN ('canceled','unavailable') AND product_value IS NOT NULL""").fetchone()
    assert bands["orders"].sum() == exp[0]
    assert bands["product_sales_value"].sum() == pytest.approx(exp[1], abs=0.01)
    assert bands["order_share"].sum() == pytest.approx(1.0)


def test_payment_band_shares_sum_to_one(con):
    p = _q(con, "q12_payments_by_order_value_band")
    shares = p[["credit_card_share", "boleto_share", "voucher_share", "debit_card_share"]].sum(axis=1)
    # not_defined payments are the only other type; shares must not exceed 1
    assert (shares <= 1.0 + 1e-9).all()


def test_new_value_and_growth_queries_run(con):
    for q in ["q10_order_value_by_category", "q11_order_value_by_state", "q13_category_growth"]:
        assert _q(con, q) is not None
