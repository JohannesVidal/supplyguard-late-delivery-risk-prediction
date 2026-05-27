-- SupplyGuard SQL Layer
-- 05_create_views.sql
-- Create safe order-level aggregation views.

USE supplyguard;

DROP VIEW IF EXISTS order_items_agg;
DROP VIEW IF EXISTS payments_agg;
DROP VIEW IF EXISTS reviews_agg;


-- 1. Order items aggregated at order level

CREATE VIEW order_items_agg AS
SELECT
    order_id,
    COUNT(order_item_id) AS order_item_count,
    COUNT(DISTINCT product_id) AS product_count,
    COUNT(DISTINCT seller_id) AS seller_count,
    ROUND(SUM(price), 2) AS total_item_price,
    ROUND(SUM(freight_value), 2) AS total_freight_value,
    ROUND(AVG(price), 2) AS avg_item_price,
    ROUND(MAX(price), 2) AS max_item_price,
    ROUND(SUM(price + freight_value), 2) AS total_order_item_value
FROM order_items
GROUP BY order_id;


-- 2. Payments aggregated at order level

CREATE VIEW payments_agg AS
WITH payment_type_counts AS (
    SELECT
        order_id,
        payment_type,
        COUNT(*) AS payment_type_count,
        ROW_NUMBER() OVER (
            PARTITION BY order_id
            ORDER BY COUNT(*) DESC, payment_type ASC
        ) AS payment_type_rank
    FROM order_payments
    GROUP BY order_id, payment_type
),
main_payment_type AS (
    SELECT
        order_id,
        payment_type AS main_payment_type
    FROM payment_type_counts
    WHERE payment_type_rank = 1
)
SELECT
    op.order_id,
    COUNT(op.payment_sequential) AS payment_count,
    COUNT(DISTINCT op.payment_type) AS payment_method_count,
    ROUND(SUM(op.payment_value), 2) AS total_payment_value,
    ROUND(AVG(op.payment_value), 2) AS avg_payment_value,
    MAX(op.payment_installments) AS max_payment_installments,
    mpt.main_payment_type
FROM order_payments op
LEFT JOIN main_payment_type mpt ON op.order_id = mpt.order_id
GROUP BY op.order_id, mpt.main_payment_type;


-- 3. Reviews aggregated at order level
-- Review data is post-delivery and should not be used as a direct ML feature.

CREATE VIEW reviews_agg AS
SELECT
    order_id,
    COUNT(review_id) AS review_count,
    ROUND(AVG(review_score), 2) AS avg_review_score,
    MIN(review_score) AS min_review_score,
    MAX(review_score) AS max_review_score,
    SUM(CASE WHEN review_comment_message IS NOT NULL AND review_comment_message <> '' THEN 1 ELSE 0 END) AS review_comment_count
FROM order_reviews
GROUP BY order_id;

USE supplyguard;

SELECT * FROM order_items_agg LIMIT 5;
SELECT * FROM payments_agg LIMIT 5;
SELECT * FROM reviews_agg LIMIT 5;