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
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    chart_dir.mkdir(parents=True, exist_ok=True)
    m = results["q01_monthly_trend"]
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(m["purchase_month"], m["orders"], color="#1f4e79")
    ax.set_title("Monthly orders (excl. canceled/unavailable)")
    ax.set_ylabel("Orders"); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "monthly_orders.png", dpi=150); plt.close(fig)

    c = results["q02_category_contribution"].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(c["category"], c["value_share"] * 100, color="#1f4e79")
    ax.set_title("Top 10 categories by share of product sales value (%)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "category_share.png", dpi=150); plt.close(fig)
