"""Generate the SYNTHETIC test fixture in tests/fixtures/. Not real Olist data.
Deterministic. Never used for business findings; it only exercises edge cases."""
import csv, random
from datetime import datetime, timedelta
from pathlib import Path

out = Path(__file__).parent / "fixtures"
out.mkdir(exist_ok=True)
rnd = random.Random(42)
F = "%Y-%m-%d %H:%M:%S"

def w(name, header, rows):
    with (out / name).open("w", newline="") as fh:
        c = csv.writer(fh); c.writerow(header); c.writerows(rows)

cats = [("cat_a", "category_a"), ("cat_b", "category_b")]
w("product_category_name_translation.csv", ["product_category_name", "product_category_name_english"], cats)
products = [(f"p{i}", ["cat_a", "cat_b", "cat_untranslated"][i % 3]) for i in range(6)]
w("olist_products_dataset.csv", ["product_id", "product_category_name"], products)
sellers = [(f"s{i}", "00000", "city", ["SP", "RJ"][i % 2]) for i in range(3)]
w("olist_sellers_dataset.csv", ["seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"], sellers)

customers, orders, items, pays, revs = [], [], [], [], []
base = datetime(2017, 1, 1)
statuses = ["delivered"] * 14 + ["canceled", "shipped"]
for i in range(60):
    cid, uid, oid = f"c{i}", f"u{i % 45}", f"o{i}"   # u0..u14 repeat customers
    customers.append((cid, uid, "01000", "city", ["SP", "RJ", "MG"][i % 3]))
    st = statuses[i % len(statuses)]
    p = base + timedelta(days=i * 5, hours=rnd.randint(0, 20))
    est = p + timedelta(days=20)
    deliv = p + timedelta(days=rnd.randint(5, 30)) if st == "delivered" else None
    if i == 3:  deliv = None                    # delivered but missing timestamp
    orders.append((oid, cid, st, p.strftime(F), (p + timedelta(hours=2)).strftime(F), "",
                   deliv.strftime(F) if deliv else "", est.strftime(F)))
    if st != "canceled" or i % 2:
        n = 1 + (i % 3)                          # 1-3 items => fan-out risk
        for k in range(1, n + 1):
            items.append((oid, k, f"p{(i + k) % 6}", f"s{(i + k) % 3}", p.strftime(F),
                          round(10 + rnd.random() * 90, 2), round(2 + rnd.random() * 10, 2)))
    for s in range(1, 1 + (i % 2) + 1):          # 1-2 payment records
        pays.append((oid, s, ["credit_card", "boleto"][s % 2], 1 + i % 4, round(20 + rnd.random() * 50, 2)))
    if i % 7:
        revs.append((f"r{i}", oid, rnd.randint(1, 5), "", "", p.strftime(F), p.strftime(F)))
    if i % 10 == 0:                              # duplicate review rows for an order
        revs.append((f"r{i}b", oid, rnd.randint(1, 5), "", "", (p + timedelta(days=1)).strftime(F), p.strftime(F)))

w("olist_customers_dataset.csv", ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"], customers)
w("olist_orders_dataset.csv", ["order_id", "customer_id", "order_status", "order_purchase_timestamp", "order_approved_at",
   "order_delivered_carrier_date", "order_delivered_customer_date", "order_estimated_delivery_date"], orders)
w("olist_order_items_dataset.csv", ["order_id", "order_item_id", "product_id", "seller_id", "shipping_limit_date", "price", "freight_value"], items)
w("olist_order_payments_dataset.csv", ["order_id", "payment_sequential", "payment_type", "payment_installments", "payment_value"], pays)
w("olist_order_reviews_dataset.csv", ["review_id", "order_id", "review_score", "review_comment_title", "review_comment_message",
   "review_creation_date", "review_answer_timestamp"], revs)
