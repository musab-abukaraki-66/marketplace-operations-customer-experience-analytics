# Findings and recommendations

All numbers come from the real Olist dataset (downloaded 2026-10-14), produced by `python -m src.pipeline` and stored in `reports/`. Unless stated otherwise: **period** is the full dataset (purchases 2016-09-04 to 2018-10-17), **active orders** exclude `canceled`/`unavailable`, and monetary values are as recorded in the data (currency not stated in the dataset).

**How to read these.** Findings are descriptive associations. Nothing here shows that one factor causes another, and "product sales value" is the sum of item prices: it is not revenue, margin or profit, and no profit statement is made. The dataset is a public, anonymised extract, so the findings describe this extract and may not generalise to the platform. The recommendations are hypotheses to investigate, addressed to the fictional stakeholders in [`business_request.md`](business_request.md).

## Findings

### F1. Order volume and product sales value were much higher in Jan-Aug 2018 than in Jan-Aug 2017, then flat within 2018
- **Source:** [`q01_monthly_trend.csv`](../reports/q01_monthly_trend.csv) (`sql/04_business_analysis/q01_monthly_trend.sql`). Population: active orders. Grain: month.
- **Comparison (same 8 calendar months, the only full months available for both years):** baseline Jan-Aug 2017 = 22,562 orders and 3,080,851 product sales value; comparison Jan-Aug 2018 = 53,531 orders (+137%) and 7,341,037 (+138%).
- Within 2018, monthly orders stayed between 6,145 (Jun) and 7,187 (Jan); Aug 2018 (6,421) is 10.7% below Jan 2018. Nov 2017 is the peak month (7,423 orders, 1,003,862) and is followed by a dip in Dec (5,620). The data does not say why; Nov 2017 contains Black Friday, but that link was not tested.
- **Caveats:** Sep 2016, Dec 2016 and Sep 2018 hold only 1-2 active orders, Oct 2016 holds 293 and Nov 2016 none (ramp-up/partial months); all are excluded from comparisons. Growth from a young marketplace cannot be extrapolated. Average order value (product value per active order with items) stays in the 124-153 range across 2017-2018 (q01), so growth came from order count, not larger baskets.

### F2. Product sales value is spread over many categories; the top five hold about 40%
- **Source:** [`q02_category_contribution.csv`](../reports/q02_category_contribution.csv). Population: active-order items, full period, 74 categories, total 13,494,400.
- Top five by product sales value: health_beauty 9.3%, watches_gifts 8.9%, bed_bath_table 7.7%, sports_leisure 7.3%, computers_accessories 6.7% (together 39.8%). The top ten reach about 62%.
- **Caveats:** Category is the item's category; item counts and order counts differ by category (q02 reports distinct orders). 13 products have untranslated categories (kept in Portuguese).

### F3. About 8% of delivered orders arrive after the estimated date; the rate varies a lot by customer state
- **Source:** [`q04_delivery_performance.csv`](../reports/q04_delivery_performance.csv). Denominator: delivery-eligible orders (delivered, both timestamps present, delivered >= purchase) = 96,470. Late = delivered after the estimated delivery date.
- Overall: 8.1% late; average purchase-to-delivery 12.6 days (median 10.2, 90th percentile 23.1; notebook section 7).
- By state (states with >= 30 eligible orders; 27 shown): highest late rate AL 23.9% (397 orders, 24.5 days), MA 19.7% (717, 21.6 days), PI 16.0% (476), CE 15.3% (1,279); lowest RO 2.9% (243), AC 3.8% (80), AM 4.1% (145), AP 4.5% (67). SP, the largest state, has 5.9% late on 40,494 orders and the shortest average delivery time, 8.8 days. AL's late rate is about four times SP's.
- **Caveats:** "Late" is measured against the platform's own estimate. Low late rates in remote states (AM, AP: 26-27 days average) may reflect generous estimates rather than fast delivery. Small states have wide uncertainty (e.g. AC n=80, AP n=67).

### F4. Late orders have much lower review scores than on-time orders (association only)
- **Source:** [`q05_reviews_vs_delay.csv`](../reports/q05_reviews_vs_delay.csv). Population: delivery-eligible orders with a review; one review per order (the most recent).
- Late: 7,661 orders, average score 2.57, 54.1% scored 1-2. On time: 88,163 orders, average 4.29, 9.2% scored 1-2. Gap: 1.73 points.
- **Caveats:** This does not show that lateness causes low scores. Reviews are voluntary (768 orders have none), and late orders differ in other ways (region, category, seller) that this comparison does not control for. Review comments were not analysed.

### F5. Few customers order more than once
- **Source:** [`q06_repeat_customers.csv`](../reports/q06_repeat_customers.csv). Population: distinct `customer_unique_id` with at least one active order, within the observed window (about Sep 2016 - Aug 2018).
- 94,990 customers; 2,888 (3.04%) placed more than one active order.
- **Caveats:** The rate only covers the observation window, so customers whose second order falls after the data ends are counted as one-time. Customers are identified by `customer_unique_id`; the same person using different details would not be linked. Not compared with any benchmark.

### F6. A group of sellers combine high late rates with enough volume to take seriously
- **Source:** [`q07_seller_performance.csv`](../reports/q07_seller_performance.csv). Population: sellers with >= 30 delivery-eligible orders: 627 of the 2,970 sellers with any eligible order. An order with several sellers counts for each.
- Mean seller late rate (unweighted) 7.7%. Highest: seller `ede0c036...` (SP) 34.0% late over 43 orders, average score 3.67; `54965bbe...` (PR) 32.1% over 73, score 3.07; `ad781527...` (SP) 31.6% over 38. Largest volume with elevated lateness: `06a2c3af...` (MA), 389 orders, 23.6% late, average score 4.02. Lowest average score among the 30 highest late rates: `1ca7077d...` (SP), 108 orders, 19.7% late, score 2.27.
- **Caveats:** With 30-100 orders, a late rate near 30% has a 95% margin of error of roughly +/-9 to +/-16 percentage points (normal approximation), so rankings are for investigation, not conclusions. The data does not show why an order was late (seller handling vs carrier vs customer location).

### F7. Small orders are most of the volume; large orders are about half of product sales value
- **Source:** [`q09_order_value_distribution.csv`](../reports/q09_order_value_distribution.csv), [`q10_order_value_by_category.csv`](../reports/q10_order_value_by_category.csv), [`q11_order_value_by_state.csv`](../reports/q11_order_value_by_state.csv). Population: active orders with >= 1 item (98,199). Order value = sum of item prices (freight excluded).
- Orders under 100 are 58.5% of orders and 22.7% of product sales value. Orders of 200 or more are 15.3% of orders and 49.9% of value; orders of 500 or more alone are 3.7% of orders and 24.8% of value.
- By dominant category (categories with >= 100 orders): median order value ranges from 21.90 (electronics) and 29.99 (telephony) up to 1,200 (computers, 181 orders). By customer state (>= 100 orders): median 79.80 in SP versus 110.32 in PB and 110.16 in PI.
- **Caveats:** A dominant category is the category of the highest-priced item in the order. Category and state medians are descriptive and do not account for product mix or shipping distance.

### F8. Larger orders are more often paid by credit card and in instalments
- **Source:** [`q12_payments_by_order_value_band.csv`](../reports/q12_payments_by_order_value_band.csv) (bands as in q09), with overall payment mix in [`q08_payments.csv`](../reports/q08_payments.csv). Population: active orders with >= 1 item and a payment record.
- Main payment type credit card: 70.4% of orders under 50 vs 82.0% of orders of 500+. Boleto falls from 23.4% to 15.6%. Share of orders with more than one instalment: 32.4% (under 50) to 76.1% (500+); average maximum instalments 1.8 to 6.2. Overall by payment value: credit card 12.5M, boleto 2.9M, voucher 0.4M, debit card 0.2M (q08).
- **Caveats:** Main payment type is the type with the largest payment in the order; orders with several payment types are counted once. Only credit-card orders show instalments in the data (other types are all 1), so the instalment pattern partly repeats the card-share pattern. Payment value can differ from price + freight (260 orders; see data quality report).

### F9. Category growth from 2017 to 2018 was uneven (12 categories analysed)
- **Source:** [`q13_category_growth.csv`](../reports/q13_category_growth.csv). Period: Jan-Aug 2018 vs Jan-Aug 2017, active-order items. Population: categories with at least 100,000 product sales value in Jan-Aug 2017 (12 categories; smaller categories are not analysed). Marketplace-wide growth over the same months was +138%.
- Faster than the marketplace: watches_gifts +243% (206k to 708k; share +2.95 points), health_beauty +211% (+2.46 points), housewares +203%, auto +170%. Slower: cool_stuff +8.9% (share -3.74 points), toys +41.8%, perfumery +43.3%, garden_tools +49.2%.
- **Caveats:** The 100,000 base threshold keeps only 12 of 74 categories, so results say nothing about small categories. Every category grew, so "declining" categories do not appear; the contrast is relative growth and share change. Causes were not tested.

## Recommendations
These are proposals to test, not conclusions. Owners are the fictional roles from the business request.

| # | Recommendation | Evidence | Rationale | Priority | Owner | Measure of success | Risk / limitation |
|---|---|---|---|---|---|---|---|
| R1 | Review delivery-time estimates and carrier performance for the high-late states (AL, MA, PI, CE, SE) | F3: AL 23.9%, MA 19.7%, PI 16.0% late vs SP 5.9% | The gap is large and the volume is meaningful (AL 397, MA 717, CE 1,279 eligible orders) | High | Logistics / operations | Late rate in those states, tracked monthly on the same definition | Cause unknown: estimate quality, carrier, seller origin and distance are not separated in the data |
| R2 | Investigate the sellers with high late rates and enough volume, starting with the largest | F6: 627 sellers with >= 30 orders; top late rates 32-34% | Late delivery is concentrated among some sellers and is associated with lower scores (F4) | High | Seller management | Seller late rate and average score vs. the platform average (8.1% late; F3) after a follow-up period | Small samples; a late order may not be the seller's fault; a fair assessment needs more data |
| R3 | Add late-delivery follow-up (proactive notification, support contact) for orders already past their estimated date | F4: late orders 2.57 vs 4.29 average score; 54% vs 9% scored 1-2 | The association is strong enough to justify testing an intervention | Medium | Customer experience | Low-score rate among late orders in a controlled test | An association only; an A/B test would be needed to show an effect |
| R4 | Track repeat purchase with a longer window and cohort view before setting targets | F5: 3.04% repeat within the observed window | The rate is low but depends on window length and customer identification | Medium | Marketing / CRM analytics | Cohort repeat rate at 6 and 12 months | Dataset window is short; no benchmark available |
| R5 | Plan payment options and instalment messaging around order value | F8: instalments on 76% of 500+ orders vs 32% under 50 | Higher-value orders lean on card instalments; boleto matters more for small orders | Low | Payments / product | Share of orders by payment type per band | Associational; no checkout data on abandoned orders |
| R6 | Monitor category mix shifts (watches_gifts, health_beauty up; cool_stuff, toys down in share) | F9 | Share shifts affect average order value and delivery mix | Low | Category management | Share change per category per quarter | Only 12 categories analysed; causes not tested |

## Open items
- Power BI dashboard visuals referenced in `requirements_traceability.md` are specified, not built (no `.pbix` exists).
- No statistical tests or confidence intervals are computed; margins of error quoted above are rough guides.
