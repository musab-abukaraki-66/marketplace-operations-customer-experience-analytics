"""Chart rendering for the README and reports. One visual style, labelled directly.

All charts are drawn from the query result DataFrames (no hard-coded numbers).
"""
from pathlib import Path

NAVY, ORANGE, RED, GREY, GREEN, LIGHT = "#1f3a5f", "#e07b39", "#c0392b", "#8a94a6", "#2e8b6a", "#e8ecf2"
INK, MUTED = "#1c2430", "#5b6677"


def _style():
    import matplotlib as mpl
    mpl.use("Agg")
    mpl.rcParams.update({
        "font.family": ["Inter", "DejaVu Sans"], "font.size": 10, "text.color": INK,
        "axes.edgecolor": "#c9d0db", "axes.labelcolor": MUTED, "xtick.color": MUTED, "ytick.color": MUTED,
        "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True, "grid.color": LIGHT,
        "grid.linewidth": 0.8, "axes.axisbelow": True, "figure.facecolor": "white", "axes.facecolor": "white",
    })


def _title(fig, title, subtitle=None):
    fig.text(0.02, 0.97, title, fontsize=14, fontweight="bold", va="top", ha="left", color=INK)
    if subtitle:
        fig.text(0.02, 0.915, subtitle, fontsize=9.5, va="top", ha="left", color=MUTED)


def _save(fig, path):
    fig.savefig(path, dpi=160, facecolor="white")
    import matplotlib.pyplot as plt
    plt.close(fig)


def _monthly(m):
    full = m[m["orders"] >= 500]          # edge months hold a handful of orders and would draw a false collapse
    return full if len(full) else m


def _monthly_panel(ax, m):
    m = _monthly(m)
    x = m["purchase_month"].astype(str).str[:7]
    ax.fill_between(range(len(m)), m["orders"], color=NAVY, alpha=0.12)
    ax.plot(range(len(m)), m["orders"], color=NAVY, lw=2.2, marker="o", ms=3.5)
    step = max(len(m) // 8, 1)
    ax.set_xticks(range(0, len(m), step)); ax.set_xticklabels(x.iloc[::step], rotation=0, fontsize=8)
    ax.set_ylim(0, m["orders"].max() * 1.18)
    peak = m["orders"].idxmax(); pi = list(m.index).index(peak)
    ax.annotate(f"peak {int(m.loc[peak, 'orders']):,}\n{x.loc[peak]}", (pi, m.loc[peak, "orders"]), (pi - 2.2, m["orders"].max() * 1.02),
                fontsize=8.5, color=INK, arrowprops=dict(arrowstyle="-", color=GREY), ha="center")
    ax.set_ylabel("Orders per month")


def _late_panel(ax, s, overall):
    s = s.sort_values("late_rate")
    colors = [RED if v > overall else NAVY for v in s["late_rate"]]
    ax.barh(s["customer_state"], s["late_rate"] * 100, color=colors, height=0.72)
    ax.axvline(overall * 100, color=INK, lw=1, ls="--")
    ax.text(overall * 100 + 0.3, 0.2, f"all-state average {overall:.1%}", fontsize=8.5, color=INK, va="bottom")
    ax.set_xlabel("Late-delivery rate (%)"); ax.grid(axis="y", visible=False)
    ax.tick_params(axis="y", labelsize=8)


def make_all(results: dict, out: Path) -> None:
    _style()
    import matplotlib.pyplot as plt
    out.mkdir(parents=True, exist_ok=True)

    # ---- 1 monthly orders
    m = results["q01_monthly_trend"]
    fig, ax = plt.subplots(figsize=(9, 4.2)); fig.subplots_adjust(top=0.80, bottom=0.12, left=0.08, right=0.97)
    _monthly_panel(ax, m)
    _title(fig, "Monthly orders", "Active orders (excl. canceled/unavailable); months with at least 500 orders")
    _save(fig, out / "monthly_orders.png")

    # ---- 2 category share
    c = results["q02_category_contribution"].head(10).iloc[::-1]
    fig, ax = plt.subplots(figsize=(9, 4.8)); fig.subplots_adjust(top=0.84, bottom=0.09, left=0.22, right=0.95)
    ax.barh(c["category"].str.replace("_", " "), c["value_share"] * 100, color=NAVY, height=0.7)
    for y, v in enumerate(c["value_share"] * 100):
        ax.text(v + 0.1, y, f"{v:.1f}%", va="center", fontsize=9, color=INK)
    ax.set_xlim(0, c["value_share"].max() * 100 * 1.15); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Share of product sales value (%)")
    _title(fig, "Top 10 categories by product sales value", "Share of item price, active orders, full period (74 categories)")
    _save(fig, out / "category_share.png")

    # ---- 3 late rate by state
    s = results["q04_delivery_performance"]
    elig = s["eligible_orders"].sum()
    overall = (s["late_rate"] * s["eligible_orders"]).sum() / elig if elig else 0.0
    fig, ax = plt.subplots(figsize=(9, 6.6)); fig.subplots_adjust(top=0.88, bottom=0.08, left=0.07, right=0.97)
    _late_panel(ax, s, overall)
    _title(fig, "Late-delivery rate by customer state", "Delivered after the estimated date; states with at least 30 eligible orders. Red = above average")
    _save(fig, out / "late_rate_by_state.png")

    # ---- 4 review by delivery outcome
    r = results["q05_reviews_vs_delay"].set_index("delivery_outcome")
    fig, axes = plt.subplots(1, 2, figsize=(9, 4)); fig.subplots_adjust(top=0.78, bottom=0.12, left=0.07, right=0.97, wspace=0.3)
    labels = [k.replace("_", " ") for k in r.index]; cols = [RED if k == "late" else NAVY for k in r.index]
    for ax, col, ttl, fmt, lim in [(axes[0], "avg_review_score", "Average review score (1-5)", "{:.2f}", 5),
                                    (axes[1], "low_score_rate", "Share scoring 1-2", "{:.1%}", 1)]:
        ax.bar(labels, r[col], color=cols, width=0.55)
        for i, v in enumerate(r[col]):
            ax.text(i, v + lim * 0.02, fmt.format(v), ha="center", fontsize=11, fontweight="bold", color=INK)
        if lim == 1:
            from matplotlib.ticker import PercentFormatter
            ax.yaxis.set_major_formatter(PercentFormatter(1.0, decimals=0))
        ax.set_ylim(0, lim * 1.12); ax.set_title(ttl, fontsize=10, color=MUTED, loc="left"); ax.grid(axis="x", visible=False)
    _title(fig, "Late deliveries have much lower review scores", "Association only (reviews are voluntary; late orders differ in other ways too)")
    _save(fig, out / "review_by_delivery.png")

    # ---- 5 order value bands
    v = results["q09_order_value_distribution"]
    fig, ax = plt.subplots(figsize=(9, 4.4)); fig.subplots_adjust(top=0.80, bottom=0.13, left=0.07, right=0.97)
    x = range(len(v)); w = 0.38
    b1 = ax.bar([i - w / 2 for i in x], v["order_share"] * 100, w, color=NAVY, label="Share of orders")
    b2 = ax.bar([i + w / 2 for i in x], v["value_share"] * 100, w, color=ORANGE, label="Share of product sales value")
    for bars in (b1, b2):
        for b in bars:
            ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.6, f"{b.get_height():.0f}%", ha="center", fontsize=9)
    ax.set_xticks(list(x)); ax.set_xticklabels(v["value_band"].str.split(": ").str[1]); ax.set_xlabel("Order value (product price)")
    ax.set_ylabel("%"); ax.legend(frameon=False, loc="upper right"); ax.grid(axis="x", visible=False)
    _title(fig, "Small orders are the volume; large orders are the value", "Active orders with at least one item")
    _save(fig, out / "order_value_bands.png")

    # ---- 6 payment mix
    p = results["q12_payments_by_order_value_band"]
    fig, ax = plt.subplots(figsize=(9, 4.6)); fig.subplots_adjust(top=0.80, bottom=0.2, left=0.07, right=0.97)
    bottom = [0.0] * len(p)
    for col, label, color in [("credit_card_share", "credit card", NAVY), ("boleto_share", "boleto", ORANGE),
                              ("voucher_share", "voucher", GREY), ("debit_card_share", "debit card", GREEN)]:
        vals = (p[col] * 100).tolist()
        ax.bar(p["value_band"].str.split(": ").str[1], vals, bottom=bottom, label=label, color=color, width=0.62)
        if col in ("credit_card_share", "boleto_share"):
            for i, (b, val) in enumerate(zip(bottom, vals)):
                ax.text(i, b + val / 2, f"{val:.0f}%", ha="center", va="center", color="white", fontsize=9, fontweight="bold")
        bottom = [b + q for b, q in zip(bottom, vals)]
    ax.set_ylim(0, 100); ax.set_ylabel("% of orders (main payment type)"); ax.set_xlabel("Order value (product price)")
    ax.legend(frameon=False, ncol=4, loc="upper center", bbox_to_anchor=(0.5, -0.16)); ax.grid(axis="x", visible=False)
    _title(fig, "Larger orders lean on credit card", "Main payment type per order-value band")
    _save(fig, out / "payment_mix_by_band.png")

    # ---- 7 overview "dashboard"
    q1 = results["q01_monthly_trend"]; q6 = results["q06_repeat_customers"].iloc[0]
    tot_orders = int(q1["orders"].sum()); tot_value = float(q1["product_sales_value"].sum())
    late_n = float(r.loc["late", "orders_with_review"]) if "late" in r.index else 0
    tiles = [("Active orders", f"{tot_orders:,}"), ("Product sales value", f"{tot_value/1e6:.1f}M"),
             ("Late deliveries", f"{overall:.1%}"), ("Late-order avg review", f"{r.loc['late','avg_review_score']:.2f}" if "late" in r.index else "n/a"),
             ("Repeat customers", f"{q6['repeat_rate']:.1%}")]
    fig = plt.figure(figsize=(14, 9.2)); fig.patch.set_facecolor("#f4f6fa")
    fig.text(0.03, 0.965, "Marketplace operations & customer experience", fontsize=19, fontweight="bold", va="top", color=INK)
    fig.text(0.03, 0.925, "Olist Brazilian E-Commerce (public dataset), Sep 2016 - Oct 2018. Generated by the pipeline from real data; association only, not revenue or profit.",
             fontsize=10, va="top", color=MUTED)
    for i, (lab, val) in enumerate(tiles):
        x0 = 0.03 + i * 0.1945
        ax = fig.add_axes([x0, 0.80, 0.18, 0.095]); ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_visible(False)
        ax.set_facecolor("white"); ax.grid(False)
        ax.text(0.06, 0.68, lab, fontsize=10, color=MUTED, transform=ax.transAxes)
        ax.text(0.06, 0.18, val, fontsize=22, fontweight="bold", color=RED if "Late" in lab else NAVY, transform=ax.transAxes)
    a1 = fig.add_axes([0.05, 0.50, 0.42, 0.24]); a1.set_facecolor("white"); _monthly_panel(a1, q1)
    a1.set_title("Monthly orders", loc="left", fontsize=11, fontweight="bold")
    a2 = fig.add_axes([0.58, 0.07, 0.38, 0.67]); a2.set_facecolor("white"); _late_panel(a2, s, overall)
    a2.set_title("Late-delivery rate by state (%)", loc="left", fontsize=11, fontweight="bold")
    a3 = fig.add_axes([0.05, 0.07, 0.19, 0.31]); a3.set_facecolor("white")
    a3.bar(labels, r["avg_review_score"], color=cols, width=0.55)
    for i, val in enumerate(r["avg_review_score"]): a3.text(i, val + 0.1, f"{val:.2f}", ha="center", fontweight="bold")
    a3.set_ylim(0, 5.5); a3.set_title("Avg review score", loc="left", fontsize=11, fontweight="bold"); a3.grid(axis="x", visible=False)
    a4 = fig.add_axes([0.30, 0.07, 0.19, 0.31]); a4.set_facecolor("white")
    a4.bar(v["value_band"].str.split(": ").str[1], v["value_share"] * 100, color=ORANGE, width=0.6)
    a4.set_title("Share of product sales value\nby order-value band (%)", loc="left", fontsize=11, fontweight="bold")
    a4.tick_params(axis="x", labelsize=8, rotation=30); a4.grid(axis="x", visible=False)
    _save(fig, out / "dashboard_overview.png")
