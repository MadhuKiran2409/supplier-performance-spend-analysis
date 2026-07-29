-- Supplier scorecard: cost 35%, delivery 40%, quality 25%
WITH base AS (
 SELECT supplier_id, SUM(quantity * unit_price) AS spend,
   AVG(CASE WHEN actual_date <= promised_date THEN 1.0 ELSE 0 END) AS otd,
   SUM(defect_qty)::numeric / NULLIF(SUM(quantity),0) AS defect_rate,
   AVG(unit_price) AS avg_price
 FROM purchase_orders GROUP BY supplier_id
), normalized AS (
 SELECT *, 100 * (1 - (avg_price-MIN(avg_price) OVER()) /
   NULLIF(MAX(avg_price) OVER()-MIN(avg_price) OVER(),0)) AS cost_score
 FROM base
)
SELECT *, ROUND((.35*cost_score + .40*100*otd + .25*100*(1-defect_rate))::numeric,1) AS weighted_score
FROM normalized ORDER BY weighted_score DESC;

-- Spend concentration and cumulative Pareto percentage
WITH supplier_spend AS (
 SELECT supplier_id, SUM(quantity * unit_price) AS spend
 FROM purchase_orders GROUP BY supplier_id
)
SELECT supplier_id, spend,
       SUM(spend) OVER (ORDER BY spend DESC) /
       SUM(spend) OVER () AS cumulative_spend_pct
FROM supplier_spend
ORDER BY spend DESC;

-- Monthly delivery trend for supplier business reviews
SELECT supplier_id, DATE_TRUNC('month', order_date) AS month,
       COUNT(*) AS orders,
       AVG(CASE WHEN actual_date <= promised_date THEN 1.0 ELSE 0 END) AS otd,
       SUM(defect_qty)::numeric / NULLIF(SUM(quantity),0) AS defect_rate
FROM purchase_orders
GROUP BY supplier_id, DATE_TRUNC('month', order_date);
