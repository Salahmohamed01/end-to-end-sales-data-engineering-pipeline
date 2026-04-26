-- Primary Keys & Indexes for dim_customers
CREATE INDEX IF NOT EXISTS idx_customers_id ON dim_customers(customer_id);
CREATE INDEX IF NOT EXISTS idx_customers_city ON dim_customers(city);

-- Indexes for dim_products
CREATE INDEX IF NOT EXISTS idx_products_id ON dim_products(product_id);
CREATE INDEX IF NOT EXISTS idx_products_category ON dim_products(category_id);

-- Indexes for dim_date
CREATE INDEX IF NOT EXISTS idx_date ON dim_date(order_date);
CREATE INDEX IF NOT EXISTS idx_date_year ON dim_date(year);
CREATE INDEX IF NOT EXISTS idx_date_month ON dim_date(month);

-- Indexes for fact_sales
CREATE INDEX IF NOT EXISTS idx_fact_order_id ON fact_sales(order_id);
CREATE INDEX IF NOT EXISTS idx_fact_customer_id ON fact_sales(customer_id);
CREATE INDEX IF NOT EXISTS idx_fact_product_id ON fact_sales(product_id);
CREATE INDEX IF NOT EXISTS idx_fact_order_date ON fact_sales(order_date);