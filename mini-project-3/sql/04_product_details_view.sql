-- =====================================================================
-- Mini-Project #3 — product_details View
-- One row per product, with pricing, margins, and total sales.
-- This view feeds the Streamlit "Urban Hamster Pricing Hub" app.
-- =====================================================================
USE DATABASE hamster;

CREATE OR REPLACE VIEW product_details AS
SELECT
    p.product_id                                   AS "Product ID",
    p.name                                         AS "Name",
    p.category                                     AS "Category",
    p.brand                                        AS "Brand",
    p.department                                   AS "Department",
    p.retail_price                                 AS "Retail Price",
    p.unit_cost                                    AS "Unit Cost",
    (p.retail_price - p.unit_cost)                 AS "Product Profit Margin",
    ROUND((p.retail_price - p.unit_cost)
          / NULLIF(p.retail_price, 0) * 100, 2)    AS "Product Profit Margin (%)",
    COALESCE(s.total_sales, 0)                     AS "Total Sales"
FROM products p
LEFT JOIN (
    -- Pre-aggregate sales to one row per product so the join stays 1:1
    -- and products that never sold still appear (Total Sales = 0).
    SELECT product_id, SUM(sale_price) AS total_sales
    FROM order_items
    GROUP BY product_id
) s ON p.product_id = s.product_id;

-- Sanity check: should return 29,120 rows (one per product).
SELECT COUNT(*) AS row_count FROM product_details;
