-- =====================================================================
-- Case Study #3 (Finance) — Business Questions
-- Answers the finance team's questions: sales growth, margin health,
-- and adherence to the cost-plus-50% pricing playbook.
-- =====================================================================
USE DATABASE hamster;

-- Q1. What was the % growth in sales between 2022 and 2023?  -> +90.7%
-- Sales = SUM(sale_price) (actual revenue), all orders included per the team's request.
SELECT
    EXTRACT(year, o.created_at)                       AS "Year",
    SUM(oi.sale_price)                               AS "Sales Total",
    LAG("Sales Total") OVER (ORDER BY "Year")        AS "Previous Year Sales",
    ROUND((("Sales Total" - "Previous Year Sales")
           / "Previous Year Sales") * 100, 1)         AS "YoY % Sales Growth"
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE "Year" = '2022' OR "Year" = '2023'
GROUP BY "Year"
ORDER BY "Year";

-- Q2. Sales by year (for the line chart). Exclude 2024 (partial data).
-- 2019: $196,829  2020: $694,406  2021: $1,315,715  2022: $2,181,672  2023: $4,159,539
SELECT
    DATE_TRUNC(year, created_at)  AS "Year",
    COUNT(order_id)               AS "Total Order Count"
FROM orders
WHERE "Year" != '2024-01-01 00:00:00.000'
GROUP BY "Year"
ORDER BY "Year";

-- Revenue by year (the version actually charted for sales growth)
SELECT
    EXTRACT(year, o.created_at)  AS "Year",
    SUM(oi.sale_price)          AS "Sales Total"
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE EXTRACT(year, o.created_at) <> 2024
GROUP BY "Year"
ORDER BY "Year";

-- Q3. How many products are we losing money on (retail price < unit cost)?  -> 0
SELECT COUNT(product_id) AS "Number of Products Losing Money"
FROM products
WHERE retail_price < unit_cost;

-- Q4. How many products deviate from the cost-plus pricing policy (markup < 50%)?  -> 4
-- (Markup = (retail - cost) / cost. All four come in at ~49% and are two-piece sets.)
SELECT
    product_id   AS "Product ID",
    brand        AS "Brand",
    name         AS "Name",
    retail_price AS "Retail Price",
    unit_cost    AS "Unit Cost",
    ROUND((("Retail Price" - "Unit Cost") / "Unit Cost") * 100, 1) AS "Percent Markup"
FROM products
WHERE (((retail_price - unit_cost) / unit_cost) * 100) < 50
ORDER BY "Percent Markup" DESC;

-- Supporting metric: average order value by year (used to show growth is volume-driven).
-- AOV holds near ~$86 every year while revenue rises ~21x -> growth comes from volume.
SELECT
    EXTRACT(year, o.created_at)                          AS "Year",
    SUM(oi.sale_price)                                  AS "Revenue",
    COUNT(DISTINCT o.order_id)                          AS "Orders",
    SUM(oi.sale_price) / COUNT(DISTINCT o.order_id)     AS "Average Order Value"
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
WHERE EXTRACT(year, o.created_at) <> 2024
GROUP BY "Year"
ORDER BY "Year";
