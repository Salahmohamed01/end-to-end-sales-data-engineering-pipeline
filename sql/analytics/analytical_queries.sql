-- 1) Total Revenue
SELECT SUM(total_amount) AS total_revenue
FROM fact_sales;

-- 2) Revenue per Year
SELECT d.year, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.order_date = d.order_date
GROUP BY d.year
ORDER BY d.year;

-- 3) Top 10 Products by Revenue
SELECT f.product_id, p.category_id, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY f.product_id
ORDER BY revenue DESC
LIMIT 10;

-- 4) Top 10 Customers by Revenue
SELECT f.customer_id, c.city, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_customers c ON f.customer_id = c.customer_id
GROUP BY f.customer_id
ORDER BY revenue DESC
LIMIT 10;

-- 5) Revenue per Category
SELECT p.category_id, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY p.category_id
ORDER BY revenue DESC;

-- 6) Monthly Revenue Trend
SELECT d.year, d.month, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_date d ON f.order_date = d.order_date
GROUP BY d.year, d.month
ORDER BY d.year, d.month;

-- 7) Average Order Value
SELECT AVG(total_amount) AS avg_order_value
FROM fact_sales;

-- View: Monthly Sales Summary
CREATE VIEW IF NOT EXISTS vw_monthly_sales AS
SELECT d.year, d.month, SUM(f.total_amount) AS revenue, COUNT(*) AS num_orders
FROM fact_sales f
JOIN dim_date d ON f.order_date = d.order_date
GROUP BY d.year, d.month;

-- View: Top Products Summary
CREATE VIEW IF NOT EXISTS vw_top_products AS
SELECT f.product_id, p.category_id, SUM(f.total_amount) AS revenue
FROM fact_sales f
JOIN dim_products p ON f.product_id = p.product_id
GROUP BY f.product_id
ORDER BY revenue DESC;