-- SupplyGuard SQL Layer
-- 03_quality_checks.sql
-- Validate row counts, primary keys, and compound keys after import.

USE supplyguard;

-- 1. Row count validation

SELECT 'category_translation' AS table_name, COUNT(*) AS rows_count FROM category_translation
UNION ALL SELECT 'customers', COUNT(*) FROM customers
UNION ALL SELECT 'geolocation_clean', COUNT(*) FROM geolocation_clean
UNION ALL SELECT 'geolocation_zip_prefix', COUNT(*) FROM geolocation_zip_prefix
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'order_payments', COUNT(*) FROM order_payments
UNION ALL SELECT 'order_reviews', COUNT(*) FROM order_reviews
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'sellers', COUNT(*) FROM sellers
ORDER BY table_name;


-- 2. Primary and compound key validation

SELECT 'customers.customer_id' AS key_check, COUNT(*) AS rows_count, COUNT(DISTINCT customer_id) AS unique_keys, COUNT(*) - COUNT(DISTINCT customer_id) AS duplicate_key_rows
FROM customers

UNION ALL SELECT 'orders.order_id', COUNT(*), COUNT(DISTINCT order_id), COUNT(*) - COUNT(DISTINCT order_id)
FROM orders

UNION ALL SELECT 'sellers.seller_id', COUNT(*), COUNT(DISTINCT seller_id), COUNT(*) - COUNT(DISTINCT seller_id)
FROM sellers

UNION ALL SELECT 'products.product_id', COUNT(*), COUNT(DISTINCT product_id), COUNT(*) - COUNT(DISTINCT product_id)
FROM products

UNION ALL SELECT 'geolocation_zip_prefix.geolocation_zip_code_prefix', COUNT(*), COUNT(DISTINCT geolocation_zip_code_prefix), COUNT(*) - COUNT(DISTINCT geolocation_zip_code_prefix)
FROM geolocation_zip_prefix

UNION ALL SELECT 'category_translation.product_category_name', COUNT(*), COUNT(DISTINCT product_category_name), COUNT(*) - COUNT(DISTINCT product_category_name)
FROM category_translation;


-- 3. Compound key validation

SELECT 'order_items.order_id + order_item_id' AS key_check, COUNT(*) AS rows_count, COUNT(DISTINCT order_id, order_item_id) AS unique_keys, COUNT(*) - COUNT(DISTINCT order_id, order_item_id) AS duplicate_key_rows
FROM order_items

UNION ALL SELECT 'order_payments.order_id + payment_sequential', COUNT(*), COUNT(DISTINCT order_id, payment_sequential), COUNT(*) - COUNT(DISTINCT order_id, payment_sequential)
FROM order_payments

UNION ALL SELECT 'order_reviews.review_id + order_id', COUNT(*), COUNT(DISTINCT review_id, order_id), COUNT(*) - COUNT(DISTINCT review_id, order_id)
FROM order_reviews;