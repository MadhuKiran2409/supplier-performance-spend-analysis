# Supplier Performance & Spend Analysis

Procurement analytics case study evaluating 15 suppliers across cost, delivery, quality, and spend concentration using 600 synthetic purchase orders.

> Data note: all records are synthetic and generated for portfolio demonstration.

## Decisions supported

- Identify preferred, watch-list, and high-risk suppliers.
- Compare on-time delivery and defect performance.
- Understand supplier-level spend exposure.
- Create a transparent weighted score: cost 35%, delivery 40%, quality 25%.

## Verified outputs

The full ranking is in [`output/supplier_scorecard.csv`](output/supplier_scorecard.csv), with headline metrics in [`output/executive_summary.csv`](output/executive_summary.csv).

![Supplier scorecard](output/supplier_scorecard.png)

## Repository

```text
data/       Supplier master and purchase-order transactions
sql/        PostgreSQL weighted-score query
src/        Python data generation and analysis
output/     Scorecard, summary, and visualization
```

## Reproduce

```bash
python -m pip install -r requirements.txt
python src/analyze_suppliers.py
```

## Skills demonstrated

Procurement analytics · Supplier management · Spend analysis · OTD · Quality · SQL · Python · KPI design · Data visualization
