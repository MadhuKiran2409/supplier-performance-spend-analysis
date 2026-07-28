# Supplier Performance & Spend Analysis

A procurement analytics project designed to evaluate supplier cost, delivery, quality, lead-time, and spend performance through one structured decision model.

> **Project status:** In development. The business scope and implementation plan are complete. Data, analysis, findings, and dashboard files will be added as each milestone is completed.

## Business Question

Which suppliers create the most value, which suppliers introduce the most risk, and where should procurement focus its improvement or sourcing efforts?

## Project Objectives

* Analyze supplier and category-level spending
* Measure purchase price variance
* Compare delivery and lead-time performance
* Evaluate supplier defect and rejection rates
* Create a weighted supplier scorecard
* Recommend suppliers for development, negotiation, or review

## Planned KPIs

| KPI                     | Business Purpose                                          |
| ----------------------- | --------------------------------------------------------- |
| Total Spend             | Shows supplier and category-level spending                |
| Spend Concentration     | Identifies dependency on individual suppliers             |
| Purchase Price Variance | Compares actual prices with an established baseline       |
| On-Time Delivery        | Measures supplier delivery reliability                    |
| Average Lead Time       | Measures supplier responsiveness                          |
| Defect Rate             | Measures incoming material quality                        |
| Supplier Score          | Combines cost, delivery, quality, and service performance |

## Technology

* **SQL:** Supplier spend, pricing, delivery, quality, and variance analysis
* **Excel and Power Query:** Data preparation, validation, and supplier scorecard testing
* **Power BI:** Supplier comparison and procurement dashboard
* **SAP MM concepts:** Purchase orders, goods receipts, invoices, and supplier data

## Planned Workflow

1. Inspect supplier, purchase order, receipt, invoice, and quality data.
2. Clean and standardize the source tables.
3. Build a supplier-level analytical dataset.
4. Calculate procurement KPIs and purchase price variance using SQL.
5. Create weighted supplier scorecard logic.
6. Validate the calculations in Excel.
7. Build a Power BI procurement dashboard.
8. Produce sourcing and supplier-management recommendations.

## Repository Structure

```text
data/          Sample data or source instructions
sql/           Procurement and supplier queries
analysis/      Excel scorecard and validation
dashboard/     Power BI file and exported visuals
docs/          Assumptions and KPI dictionary
README.md      Project story and final recommendations
```

## Expected Deliverables

* Cleaned procurement dataset
* Supplier and spend SQL scripts
* Weighted supplier scorecard
* Power BI procurement dashboard
* KPI definitions and data dictionary
* Executive recommendation summary

## Skills Demonstrated

Procure-to-Pay · Supplier Management · Spend Analytics · SQL · Excel · Power Query · Power BI · SAP MM Concepts

## Next Milestone

Add a realistic purchase-order dataset and complete the initial spend-concentration analysis.
