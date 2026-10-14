-- Each row: check name, failing record count, severity ('error' fails the pipeline).
SELECT 'orders_duplicate_order_id' AS check_name, 'error' AS severity,
       (SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM clean_orders) AS failing_rows
UNION ALL SELECT 'customers_duplicate_customer_id','error',
       (SELECT COUNT(*) - COUNT(DISTINCT customer_id) FROM clean_customers)
UNION ALL SELECT 'items_duplicate_pk','error',
       (SELECT COUNT(*) - COUNT(DISTINCT (order_id, order_item_id)) FROM clean_order_items)
UNION ALL SELECT 'fact_orders_rowcount_mismatch','error',
       (SELECT ABS((SELECT COUNT(*) FROM fact_orders) - (SELECT COUNT(*) FROM clean_orders)))
UNION ALL SELECT 'items_orphan_order_fk','error',
       (SELECT COUNT(*) FROM clean_order_items i ANTI JOIN clean_orders o USING (order_id))
UNION ALL SELECT 'payments_orphan_order_fk','error',
       (SELECT COUNT(*) FROM clean_payments p ANTI JOIN clean_orders o USING (order_id))
UNION ALL SELECT 'orders_orphan_customer_fk','error',
       (SELECT COUNT(*) FROM clean_orders o ANTI JOIN clean_customers c USING (customer_id))
UNION ALL SELECT 'negative_or_null_price','error',
       (SELECT COUNT(*) FROM clean_order_items WHERE price IS NULL OR price < 0 OR freight_value IS NULL OR freight_value < 0)
UNION ALL SELECT 'product_value_reconciliation_diff','error',
       (SELECT CAST(ABS((SELECT SUM(product_value) FROM fact_orders) - (SELECT SUM(price) FROM clean_order_items)) > 0.01 AS INTEGER))
UNION ALL SELECT 'freight_reconciliation_diff','error',
       (SELECT CAST(ABS((SELECT SUM(freight_value) FROM fact_orders) - (SELECT SUM(freight_value) FROM clean_order_items)) > 0.01 AS INTEGER))
UNION ALL SELECT 'payment_reconciliation_diff','error',
       (SELECT CAST(ABS((SELECT SUM(payment_value) FROM fact_orders) - (SELECT SUM(payment_value) FROM clean_payments)) > 0.01 AS INTEGER))
UNION ALL SELECT 'review_score_out_of_range','error',
       (SELECT COUNT(*) FROM clean_reviews WHERE review_score IS NOT NULL AND review_score NOT BETWEEN 1 AND 5)
UNION ALL SELECT 'unparseable_purchase_ts','error',
       (SELECT COUNT(*) FROM clean_orders WHERE purchase_ts IS NULL)
-- Informational (documented, not failing): affect KPI denominators.
UNION ALL SELECT 'info_delivered_missing_delivery_ts','info',
       (SELECT COUNT(*) FROM clean_orders WHERE order_status='delivered' AND delivered_ts IS NULL)
UNION ALL SELECT 'info_delivered_before_purchase','info',
       (SELECT COUNT(*) FROM clean_orders WHERE delivered_ts < purchase_ts)
UNION ALL SELECT 'info_orders_without_items','info',
       (SELECT COUNT(*) FROM fact_orders WHERE item_count IS NULL)
UNION ALL SELECT 'info_orders_without_review','info',
       (SELECT COUNT(*) FROM fact_orders WHERE review_score IS NULL)
UNION ALL SELECT 'info_duplicate_orders_in_reviews','info',
       (SELECT COUNT(*) - COUNT(DISTINCT order_id) FROM clean_reviews)
UNION ALL SELECT 'info_untranslated_categories','info',
       (SELECT COUNT(*) FROM clean_products WHERE category_untranslated)
UNION ALL SELECT 'info_unknown_status','info',
       (SELECT COUNT(*) FROM clean_orders WHERE order_status NOT IN
        ('delivered','shipped','canceled','unavailable','invoiced','processing','created','approved'));
