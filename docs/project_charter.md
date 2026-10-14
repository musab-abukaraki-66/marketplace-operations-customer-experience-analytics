# Project charter

| Item | Content |
|---|---|
| Context | Simulated marketplace leadership request (see `business_request.md`). Data: public Olist orders, 2016–2018 (verify exact range after download; the pipeline derives it from the data). |
| Problem | Leadership lacks a consistent, trusted view of commercial, delivery and customer-experience performance. |
| Objectives | (1) Define governed KPIs. (2) Quantify trends, delivery reliability, review outcomes, repeat purchasing. (3) Identify segments/sellers worth investigating. (4) Deliver a dashboard and a short recommendation set. |
| Stakeholders | Marketplace leadership (decisions); Operations/Logistics; Customer Experience; Seller Management (intended users). |
| In scope | Order, item, payment, review, product, seller, customer tables; SQL/Python pipeline; Power BI model and DAX; findings report. |
| Out of scope | Profit, margin, CLV, cost savings (no cost data); forecasting/ML; causal claims; text analysis of reviews; geolocation table. |
| Deliverables | Pipeline + SQL, KPI dictionary, quality report, traceability matrix, Power BI model spec, findings report. |
| Assumptions | Dataset is a historical, anonymised sample; `customer_unique_id` identifies a person; one review per order after dedup rule. |
| Risks | Sample-size noise for small sellers/categories; missing timestamps; reviews are voluntary (selection bias); no data after 2018. |
| Success | Every KPI has a definition, a tested SQL implementation and reconciled totals; every finding cites a query output; limitations are visible. |

## Required decisions
Where to focus delivery-improvement effort; which segments need seller/customer-experience follow-up; whether retention is a priority.
