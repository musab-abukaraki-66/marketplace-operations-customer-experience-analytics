# DAX measures (not yet executed in Power BI Desktop)

```dax
Total Orders = DISTINCTCOUNT ( fact_orders[order_id] )
Active Orders = CALCULATE ( [Total Orders], NOT ( fact_orders[order_status] IN { "canceled", "unavailable" } ) )
Canceled Rate = DIVIDE ( CALCULATE ( [Total Orders], fact_orders[order_status] = "canceled" ), [Total Orders] )
Product Sales Value = CALCULATE ( SUM ( fact_orders[product_value] ), NOT ( fact_orders[order_status] IN { "canceled", "unavailable" } ) )
Freight Value = CALCULATE ( SUM ( fact_orders[freight_value] ), NOT ( fact_orders[order_status] IN { "canceled", "unavailable" } ) )
AOV = DIVIDE ( [Product Sales Value],
    CALCULATE ( [Total Orders], NOT ( fact_orders[order_status] IN { "canceled", "unavailable" } ), NOT ISBLANK ( fact_orders[product_value] ) ) )
MoM Order Growth = VAR prev = CALCULATE ( [Active Orders], DATEADD ( dim_date[date_key], -1, MONTH ) )
    RETURN DIVIDE ( [Active Orders] - prev, prev )
Eligible Deliveries = CALCULATE ( [Total Orders], fact_orders[delivery_eligible] = TRUE () )
Late Rate = DIVIDE ( CALCULATE ( [Total Orders], fact_orders[delivery_eligible] = TRUE (), fact_orders[is_late] = TRUE () ), [Eligible Deliveries] )
On-Time Rate = 1 - [Late Rate]
Avg Delivery Days = CALCULATE ( AVERAGE ( fact_orders[delivery_days] ), fact_orders[delivery_eligible] = TRUE () )
Avg Review Score = AVERAGE ( fact_orders[review_score] )
Low Score Rate = DIVIDE ( CALCULATE ( [Total Orders], fact_orders[review_score] <= 2 ), CALCULATE ( [Total Orders], NOT ISBLANK ( fact_orders[review_score] ) ) )
Category Share = DIVIDE ( SUM ( fact_order_items[price] ), CALCULATE ( SUM ( fact_order_items[price] ), ALL ( fact_order_items[category] ) ) )
Repeat Rate = VAR c = SUMMARIZE ( FILTER ( fact_orders, NOT ( fact_orders[order_status] IN { "canceled", "unavailable" } ) ),
        fact_orders[customer_unique_id], "n", DISTINCTCOUNT ( fact_orders[order_id] ) )
    RETURN DIVIDE ( COUNTROWS ( FILTER ( c, [n] > 1 ) ), COUNTROWS ( c ) )
```
Minimum-volume safeguard for seller visuals: add a visual-level filter `[Eligible Deliveries] >= 30`.
Payment-type distribution requires payment-record grain, which is not in this model; either add a `fact_payments` table (order_id → fact_orders) or use the q08 export.
