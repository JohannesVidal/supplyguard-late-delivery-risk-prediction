-- SupplyGuard SQL Layer
-- 04_relationship_checks.sql
-- Validate the main relationships between SQL tables.

USE supplyguard;

SELECT 'orders.customer_id -> customers.customer_id' AS relationship, COUNT(*) AS left_rows, SUM(o.customer_id IS NULL) AS null_fk_rows,
       SUM(o.customer_id IS NOT NULL AND c.customer_id IS NULL) AS unmatched_non_null_rows,
       ROUND(SUM(o.customer_id IS NOT NULL AND c.customer_id IS NULL) / COUNT(*) * 100, 4) AS unmatched_pct,
       CASE WHEN SUM(o.customer_id IS NOT NULL AND c.customer_id IS NULL) = 0 THEN 'Pass' ELSE 'Review' END AS status
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id

UNION ALL

SELECT 'order_items.order_id -> orders.order_id', COUNT(*), SUM(oi.order_id IS NULL),
       SUM(oi.order_id IS NOT NULL AND o.order_id IS NULL),
       ROUND(SUM(oi.order_id IS NOT NULL AND o.order_id IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(oi.order_id IS NOT NULL AND o.order_id IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM order_items oi
LEFT JOIN orders o ON oi.order_id = o.order_id

UNION ALL

SELECT 'order_items.product_id -> products.product_id', COUNT(*), SUM(oi.product_id IS NULL),
       SUM(oi.product_id IS NOT NULL AND p.product_id IS NULL),
       ROUND(SUM(oi.product_id IS NOT NULL AND p.product_id IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(oi.product_id IS NOT NULL AND p.product_id IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id

UNION ALL

SELECT 'order_items.seller_id -> sellers.seller_id', COUNT(*), SUM(oi.seller_id IS NULL),
       SUM(oi.seller_id IS NOT NULL AND s.seller_id IS NULL),
       ROUND(SUM(oi.seller_id IS NOT NULL AND s.seller_id IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(oi.seller_id IS NOT NULL AND s.seller_id IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM order_items oi
LEFT JOIN sellers s ON oi.seller_id = s.seller_id

UNION ALL

SELECT 'order_payments.order_id -> orders.order_id', COUNT(*), SUM(op.order_id IS NULL),
       SUM(op.order_id IS NOT NULL AND o.order_id IS NULL),
       ROUND(SUM(op.order_id IS NOT NULL AND o.order_id IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(op.order_id IS NOT NULL AND o.order_id IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM order_payments op
LEFT JOIN orders o ON op.order_id = o.order_id

UNION ALL

SELECT 'order_reviews.order_id -> orders.order_id', COUNT(*), SUM(r.order_id IS NULL),
       SUM(r.order_id IS NOT NULL AND o.order_id IS NULL),
       ROUND(SUM(r.order_id IS NOT NULL AND o.order_id IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(r.order_id IS NOT NULL AND o.order_id IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM order_reviews r
LEFT JOIN orders o ON r.order_id = o.order_id

UNION ALL

SELECT 'customers.customer_zip_code_prefix -> geolocation_zip_prefix.geolocation_zip_code_prefix', COUNT(*), SUM(c.customer_zip_code_prefix IS NULL),
       SUM(c.customer_zip_code_prefix IS NOT NULL AND g.geolocation_zip_code_prefix IS NULL),
       ROUND(SUM(c.customer_zip_code_prefix IS NOT NULL AND g.geolocation_zip_code_prefix IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(c.customer_zip_code_prefix IS NOT NULL AND g.geolocation_zip_code_prefix IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM customers c
LEFT JOIN geolocation_zip_prefix g ON c.customer_zip_code_prefix = g.geolocation_zip_code_prefix

UNION ALL

SELECT 'sellers.seller_zip_code_prefix -> geolocation_zip_prefix.geolocation_zip_code_prefix', COUNT(*), SUM(s.seller_zip_code_prefix IS NULL),
       SUM(s.seller_zip_code_prefix IS NOT NULL AND g.geolocation_zip_code_prefix IS NULL),
       ROUND(SUM(s.seller_zip_code_prefix IS NOT NULL AND g.geolocation_zip_code_prefix IS NULL) / COUNT(*) * 100, 4),
       CASE WHEN SUM(s.seller_zip_code_prefix IS NOT NULL AND g.geolocation_zip_code_prefix IS NULL) = 0 THEN 'Pass' ELSE 'Review' END
FROM sellers s
LEFT JOIN geolocation_zip_prefix g ON s.seller_zip_code_prefix = g.geolocation_zip_code_prefix;