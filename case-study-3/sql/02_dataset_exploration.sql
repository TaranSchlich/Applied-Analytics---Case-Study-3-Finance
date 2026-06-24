-- =====================================================================
-- Case Study #3 (Finance) — Exploratory Data Analysis
-- Profiles the product catalog before answering the business questions:
-- counts, uniqueness, category/brand mix, pricing, margins, and logistics.
-- =====================================================================
USE DATABASE hamster;

-- How many products do we have?  -> 29,120
SELECT COUNT(DISTINCT product_id) AS "Total Product Count"
FROM products;

-- Are both the product IDs and SKUs unique in this table?  -> Yes (both 29,120)
SELECT
    COUNT(DISTINCT product_id) AS "Total Product Count",
    COUNT(DISTINCT sku)        AS "Total SKU Count"
FROM products;

-- Which three categories include the most products?  -> Intimates, Jeans, Tops & Tees
SELECT
    category                      AS "Product Category",
    COUNT(DISTINCT product_id)    AS "Total Product Count per Category"
FROM products
GROUP BY "Product Category"
ORDER BY "Total Product Count per Category" DESC
LIMIT 3;

-- How many products are in the top category?  -> Intimates, 2,363
SELECT
    category                      AS "Product Category",
    COUNT(DISTINCT product_id)    AS "Total Product Count per Category"
FROM products
GROUP BY "Product Category"
ORDER BY "Total Product Count per Category" DESC
LIMIT 1;

-- Which product categories have an average retail price greater than $100?
SELECT
    category               AS "Product Category",
    AVG(retail_price)      AS "Average Retail Price by Product Category"
FROM products
GROUP BY "Product Category"
HAVING AVG(retail_price) > 100
ORDER BY "Average Retail Price by Product Category" DESC;

-- What was the highest average retail price across the product categories?  -> $146 (Outerwear & Coats)
SELECT
    category                       AS "Product Category",
    ROUND(AVG(retail_price), 0)    AS "Average Retail Price by Product Category"
FROM products
GROUP BY "Product Category"
HAVING AVG(retail_price) > 100
ORDER BY "Average Retail Price by Product Category" DESC
LIMIT 1;

-- How many different brands are we offering products from?  -> 2,756
SELECT COUNT(DISTINCT brand) AS "Number of Unique Brand Offerings"
FROM products;

-- From which three brands are we offering the most products?  -> Allegra K, Calvin Klein, Carhartt
SELECT
    brand                         AS "Brand",
    COUNT(DISTINCT product_id)    AS "Total Product Count"
FROM products
GROUP BY "Brand"
ORDER BY "Total Product Count" DESC
LIMIT 3;

-- Which brands have an average retail price greater than $600?  -> Nobis, Bergama, Jordan
SELECT
    brand               AS "Brand",
    AVG(retail_price)   AS "Average Retail Price by Brand"
FROM products
GROUP BY "Brand"
HAVING AVG(retail_price) > 600
ORDER BY "Average Retail Price by Brand" DESC;

-- Which product has the highest profit margin (in dollars)?  -> Alpha Industries "Darla" ($594.40)
SELECT
    brand,
    name,
    retail_price,
    unit_cost,
    (retail_price - unit_cost) AS "Profit Margin in Dollars"
FROM products
ORDER BY "Profit Margin in Dollars" DESC
LIMIT 1;

-- Which distribution center contains the most distinct products?  -> Chicago IL (3,929)
SELECT
    dc.name                       AS "Distribution Center Location",
    COUNT(DISTINCT p.product_id)  AS "Total Product Count"
FROM distribution_centers dc
JOIN products p ON dc.id = p.distribution_center_id
GROUP BY "Distribution Center Location"
ORDER BY "Total Product Count" DESC
LIMIT 1;
