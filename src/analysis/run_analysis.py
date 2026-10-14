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
    # Edge months of the dataset hold only a handful of orders (partial/ramp-up periods) and would
    # draw a false collapse; chart only months with a meaningful volume.
    full = m[m["orders"] >= 500]
    m = full if len(full) else m
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(m["purchase_month"], m["orders"], color="#1f4e79", marker="o", markersize=3)
    ax.set_title("Monthly orders (excl. canceled/unavailable; months with >= 500 orders)")
    ax.set_ylabel("Orders"); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "monthly_orders.png", dpi=150); plt.close(fig)

    c = results["q02_category_contribution"].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(c["category"], c["value_share"] * 100, color="#1f4e79")
    ax.set_title("Top 10 categories by share of product sales value (%)")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "category_share.png", dpi=150); plt.close(fig)

    s = results["q04_delivery_performance"].sort_values("late_rate")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.barh(s["customer_state"], s["late_rate"] * 100, color="#1f4e79")
    ax.set_title("Late-delivery rate by customer state (%), states with >= 30 eligible orders")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "late_rate_by_state.png", dpi=150); plt.close(fig)

    r = results["q05_reviews_vs_delay"]
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(r["delivery_outcome"], r["avg_review_score"], color="#1f4e79")
    ax.set_ylim(0, 5); ax.set_ylabel("Average review score")
    ax.set_title("Review score by delivery outcome")
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "review_by_delivery.png", dpi=150); plt.close(fig)

    v = results["q09_order_value_distribution"]
    x = range(len(v))
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar([i - 0.2 for i in x], v["order_share"] * 100, width=0.4, color="#1f4e79", label="Share of orders")
    ax.bar([i + 0.2 for i in x], v["value_share"] * 100, width=0.4, color="#e07b39", label="Share of product sales value")
    ax.set_xticks(list(x)); ax.set_xticklabels(v["value_band"]); ax.set_ylabel("%")
    ax.set_title("Order-value bands: share of orders vs share of value")
    ax.legend(frameon=False); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "order_value_bands.png", dpi=150); plt.close(fig)

    p = results["q12_payments_by_order_value_band"]
    fig, ax = plt.subplots(figsize=(8, 4))
    bottom = [0.0] * len(p)
    for col, label, color in [("credit_card_share", "credit card", "#1f4e79"), ("boleto_share", "boleto", "#e07b39"),
                              ("voucher_share", "voucher", "#7f7f7f"), ("debit_card_share", "debit card", "#59a14f")]:
        vals = (p[col] * 100).tolist()
        ax.bar(p["value_band"], vals, bottom=bottom, label=label, color=color)
        bottom = [b + v_ for b, v_ in zip(bottom, vals)]
    ax.set_ylabel("% of orders (main payment type)")
    ax.set_title("Main payment type by order-value band")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.12)); ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout(); fig.savefig(chart_dir / "payment_mix_by_band.png", dpi=150); plt.close(fig)
