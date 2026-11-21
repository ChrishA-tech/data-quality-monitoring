# Build the Power BI report yourself (Power BI Desktop, ~1 hour)
1. Get Data > Text/CSV: fact_orders, dim_product, dim_country, dim_channel, dim_date, root_cause_amount, dq_log.
2. Model view: fact_orders[product_key/country_key/channel_key/date_key] -> matching dim keys (many-to-one, single direction).
3. Measures:
```
Orders = COUNTROWS(fact_orders)
Missing Amount % = DIVIDE(SUM(fact_orders[is_missing_amount]), [Orders])
Duplicate Rows = SUM(fact_orders[is_duplicate])
Failed Checks = CALCULATE(COUNTROWS(dq_log), dq_log[failed] = 1)
```
4. Pareto page: bar of root_cause_amount[bad_rows] by value, sorted descending, plus a cumulative % measure:
```
Cum % = DIVIDE(CALCULATE(SUM(root_cause_amount[bad_rows]), TOPN(RANKX(ALL(root_cause_amount[value]), [Bad Rows]), ALL(root_cause_amount[value]))), SUM(root_cause_amount[bad_rows]))
```
   (simplest: sort descending and add a running total in a visual calculation).
5. Page 2: Missing Amount % by channel (store should stand out), Failed Checks card, dq_log table.
