# Applied Analytics — Case Study 3: Finance

> Analyzing Urban Hamster's sales growth and pricing discipline with SQL, then shipping a Streamlit pricing tool that arms the sales team for vendor negotiations.

---

## Project Overview

Urban Hamster, a fictional apparel retailer, is the basis for a multi-part applied analytics case study series. This repository covers **Case Study 3**, where the central analytics team was engaged by the **Finance** department to quantify sales growth, audit pricing and margins, and then build an internal tool to support vendor negotiations.

The work spans two connected phases — from raw SQL analysis through a stakeholder presentation, then a data app:

| Phase | Folder | Deliverable |
|---|---|---|
| Case Study 3 — finance analysis (growth, margins, pricing policy) | [`case-study-3/`](./case-study-3) | [Finance Findings deck](./case-study-3/deliverables/Urban_Hamster_Case3_Finance_Findings.pptx) + [video walkthrough](./case-study-3/deliverables/VIDEO.md) |
| Mini-Project 3 — Streamlit "Pricing Hub" app for the sales team | [`mini-project-3/`](./mini-project-3) | [Streamlit app](./mini-project-3/streamlit/streamlit_app.py) · [live app ↗](https://app.snowflake.com/streamlit/us-east-1/eac82456/#/apps/lgxwayv44dmv53cfrhdp) · [video walkthrough](./mini-project-3/deliverables/VIDEO.md) |

---

## Business Context

Senior finance manager **Kent** raised the following questions:

- How much did sales grow last year versus the year before?
- Which products carry weak margins — how many cost us more to sell than they should?
- Are we adhering to our pricing playbook (**cost plus a 50% markup**)? Are we leaving money on the table, or running a sale we never intended?
- How do our prices hold up against competitors, so we can align with both our costs and the market?

After the analysis, Kent's follow-up: the sales staff negotiate product costs with clothing vendors regularly, and they want **better product information going into those negotiations** — a tool showing pricing, margins, and revenue, filterable by department, category, and brand.

---

## Key Findings

### Phase 1 — Finance Analysis

| Question | Answer |
|---|---|
| Sales growth, 2022 → 2023 | **+90.7%** ($2.18M → $4.16M) |
| Five-year trajectory | $197K (2019) → $4.16M (2023) — **~21×**, growth re-accelerated from +65.8% to +90.7% |
| What's driving growth | **Volume, not price** — average order value held near **$86** every year, so ~96% of growth came from more orders |
| Products sold below cost | **0** |
| Products off the cost-plus-50% rule | **4 of 29,120 (0.01%)** — all at ~49%, and all **two-piece sets** |
| Highest-margin product | Alpha Industries "Darla" — **$594.40**/unit |

**Recommendation:** Pricing is disciplined but anchored to cost, not the market — and the policy only checks list price, not what we actually collect after discounts. The next dollar of margin comes from **benchmarking against competitors** (start with top-revenue and high-ticket products; source pricing from the Snowflake Marketplace) and **tracking realized margin** (`sale_price` vs. cost).

### Catalog context (exploratory analysis)

- **29,120 products** across **2,756 brands** and **10 distribution centers** (largest: Chicago, IL — 3,929 products)
- Largest categories: **Intimates (2,363), Jeans (1,999), Tops & Tees (1,868)**
- Highest average retail price by category: **Outerwear & Coats ($146)**; top brand by count: **Allegra K (1,034)**

### Phase 2 — Mini-Project 3: Pricing Hub App

- Built a `product_details` **view** (one row per product: price, unit cost, margin in $ and %, total sales) feeding a **Streamlit-in-Snowflake** app
- The **Urban Hamster Pricing Hub** lets sales filter by department, category, and brand; it surfaces 4 KPIs, three Seaborn distributions, and a filtered data table — all reactive to the filters
  - 🔗 **Live app:** [Streamlit in Snowflake](https://app.snowflake.com/streamlit/us-east-1/eac82456/#/apps/lgxwayv44dmv53cfrhdp) *(requires access to the Snowflake workspace)*
- Includes the introductory **Retirement Calculator** warm-up (sample inputs → **$3,330,503.40**)

---

## Tech Stack

- **SQL / Snowflake** — data exploration, business-question analysis, and the `product_details` view
- **Python** — `pandas`, `seaborn`, `matplotlib` (charts), `python-pptx` (branded deck generation)
- **Streamlit in Snowflake** — the interactive Pricing Hub app
- **PowerPoint** — stakeholder-facing findings presentation
- **Video** — recorded walkthroughs for non-technical stakeholders

---

## Repository Structure

```
.
├── case-study-3/                  # Phase 1 — finance analysis
│   ├── sql/
│   │   ├── 01_database_setup.sql        # Snowflake DB, tables, stage, data load
│   │   ├── 02_dataset_exploration.sql   # Exploratory profiling queries
│   │   └── 03_business_questions.sql    # Growth, margin, and pricing-policy queries
│   ├── results/
│   │   └── GB884_Case_3_Query_Results.xlsx   # Query outputs from Snowflake
│   ├── visuals/                         # Generated charts (revenue, AOV, markup)
│   ├── scripts/                         # Python used to build the charts + deck
│   │   ├── generate_charts.py
│   │   └── build_deck.py
│   └── deliverables/
│       ├── Urban_Hamster_Case3_Finance_Findings.pptx
│       └── VIDEO.md                     # Presentation speaker notes
│
├── mini-project-3/                # Phase 2 — Streamlit app
│   ├── sql/
│   │   └── 04_product_details_view.sql  # View feeding the app
│   ├── streamlit/
│   │   └── streamlit_app.py             # Urban Hamster Pricing Hub
│   ├── retirement-calculator/
│   │   └── streamlit_app.py             # Intro Streamlit warm-up
│   ├── data/
│   │   └── product_details_view.csv     # Exported view data (29,120 rows)
│   └── deliverables/
│       └── VIDEO.md                     # App walkthrough notes
│
└── README.md
```

---

## Reproducing the Analysis

The SQL assumes a Snowflake database named `hamster` with the standard `users`, `orders`, `order_items`, `products`, `distribution_centers`, and `events` tables (created and loaded by [`01_database_setup.sql`](./case-study-3/sql/01_database_setup.sql)). Run the SQL in order (`01` → `04`), then deploy `mini-project-3/streamlit/streamlit_app.py` as a Streamlit-in-Snowflake app on the `hamster` database.

Code is provided for transparency and reproducibility — but per stakeholder preference, the findings deck and app walkthroughs are presentation-ready and contain no code.

---

*Coursework for GB884 — Applied Analytics. Author: T. Schlichtmann.*
