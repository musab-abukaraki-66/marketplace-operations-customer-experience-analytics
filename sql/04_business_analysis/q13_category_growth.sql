-- BQ2 (growth): category product sales value, Jan-Aug 2018 vs Jan-Aug 2017.
-- Same 8 calendar months in both years (the dataset ends mid-Aug/Sep 2018, so later months are
-- partial). Active orders only. Categories need >= 100,000 base-period value to avoid tiny-base
-- percentages. share_change_pp = change in the category's share of total value, in points
-- (marketplace-wide growth is large, so share change is more informative than raw growth).
WITH per_cat AS (
  SELECT category,
         SUM(price) FILTER (WHERE purchase_month BETWEEN DATE '2017-01-01' AND DATE '2017-08-01') AS value_2017,
         SUM(price) FILTER (WHERE purchase_month BETWEEN DATE '2018-01-01' AND DATE '2018-08-01') AS value_2018
  FROM fact_order_items
  WHERE order_status NOT IN ('canceled', 'unavailable')
  GROUP BY 1),
tot AS (SELECT SUM(value_2017) AS t17, SUM(value_2018) AS t18 FROM per_cat)
SELECT category, value_2017, value_2018,
       value_2018 / value_2017 - 1                         AS growth_rate,
       (value_2018 / t18 - value_2017 / t17) * 100         AS share_change_pp
FROM per_cat, tot
WHERE value_2017 >= 100000 AND value_2018 IS NOT NULL
ORDER BY growth_rate DESC;
