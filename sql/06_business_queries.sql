-- SupplyGuard SQL Layer
-- 06_business_queries.sql
-- Reusable business queries for future analysis.
-- Official late delivery definition: date-only comparison.

USE supplyguard;

-- Note:
-- These queries are designed for historical business analysis.
-- The late delivery flag uses actual delivery information and should be treated as target logic,
-- not as a direct feature source for future machine learning.


-- 1. Order-level analytical base using safe aggregated views


SELECT
    o.order_id,
    o.customer_id,
    c.customer_state,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_approved_at,
    o.order_estimated_delivery_date,
    o.order_delivered_customer_date,
    DATE(o.order_delivered_customer_date) AS delivered_date,
    DATE(o.order_estimated_delivery_date) AS estimated_delivery_date,
    oi.order_item_count,
    oi.product_count,
    oi.seller_count,
    oi.total_item_price,
    oi.total_freight_value,
    p.payment_count,
    p.payment_method_count,
    p.main_payment_type,
    p.total_payment_value,
    CASE
        WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) THEN 1
        ELSE 0
    END AS is_late
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
LEFT JOIN order_items_agg oi ON o.order_id = oi.order_id
LEFT JOIN payments_agg p ON o.order_id = p.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
LIMIT 100;


-- 2. Historical late delivery overview


SELECT
    COUNT(*) AS delivered_orders_analyzed,
    SUM(CASE WHEN DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date) THEN 1 ELSE 0 END) AS late_orders,
    ROUND(AVG(CASE WHEN DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date) THEN 1 ELSE 0 END) * 100, 2) AS late_delivery_rate_pct
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;

-- Methodology check: timestamp-based vs date-only late delivery definition

SELECT
    COUNT(*) AS delivered_orders_analyzed,
    SUM(CASE WHEN order_delivered_customer_date > order_estimated_delivery_date THEN 1 ELSE 0 END) AS timestamp_based_late_orders,
    SUM(CASE WHEN DATE(order_delivered_customer_date) > DATE(order_estimated_delivery_date) THEN 1 ELSE 0 END) AS date_only_late_orders,
    SUM(CASE
        WHEN order_delivered_customer_date > order_estimated_delivery_date
         AND DATE(order_delivered_customer_date) <= DATE(order_estimated_delivery_date)
        THEN 1 ELSE 0
    END) AS timestamp_only_late_orders
FROM orders
WHERE order_status = 'delivered'
  AND order_delivered_customer_date IS NOT NULL
  AND order_estimated_delivery_date IS NOT NULL;

-- 3. Late delivery rate by customer state


SELECT
    c.customer_state,
    COUNT(*) AS delivered_orders,
    SUM(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) THEN 1 ELSE 0 END) AS late_orders,
    ROUND(AVG(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) THEN 1 ELSE 0 END) * 100, 2) AS late_delivery_rate_pct
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY c.customer_state
ORDER BY late_delivery_rate_pct DESC;


-- 4. Late delivery rate by seller state

WITH order_seller_state AS (
    SELECT DISTINCT
        oi.order_id,
        s.seller_state
    FROM order_items oi
    LEFT JOIN sellers s ON oi.seller_id = s.seller_id
)

SELECT
    oss.seller_state,
    COUNT(*) AS delivered_order_seller_pairs,
    SUM(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) THEN 1 ELSE 0 END) AS late_orders,
    ROUND(AVG(CASE WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) THEN 1 ELSE 0 END) * 100, 2) AS late_delivery_rate_pct
FROM order_seller_state oss
LEFT JOIN orders o ON oss.order_id = o.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
GROUP BY oss.seller_state
ORDER BY late_delivery_rate_pct DESC;


-- 5. Product categories by item revenue

SELECT
    p.product_category_name_english,
    COUNT(*) AS item_rows,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.price), 2) AS total_item_revenue,
    ROUND(AVG(oi.price), 2) AS avg_item_price
FROM order_items oi
LEFT JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_category_name_english
ORDER BY total_item_revenue DESC;


-- 6. Payment profile by main payment type

SELECT
    main_payment_type,
    COUNT(*) AS orders,
    ROUND(AVG(total_payment_value), 2) AS avg_total_payment_value,
    ROUND(AVG(max_payment_installments), 2) AS avg_max_installments
FROM payments_agg
GROUP BY main_payment_type
ORDER BY orders DESC;


-- 7. Review score by delivery outcome
-- Post-delivery diagnostic analysis only. Not suitable as a direct ML feature.

SELECT
    CASE
        WHEN DATE(o.order_delivered_customer_date) > DATE(o.order_estimated_delivery_date) THEN 'Late'
        ELSE 'On time'
    END AS delivery_outcome,
    COUNT(*) AS reviewed_orders,
    ROUND(AVG(r.avg_review_score), 2) AS avg_review_score,
    ROUND(AVG(r.review_comment_count), 2) AS avg_review_comment_count
FROM orders o
LEFT JOIN reviews_agg r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
  AND o.order_delivered_customer_date IS NOT NULL
  AND o.order_estimated_delivery_date IS NOT NULL
  AND r.avg_review_score IS NOT NULL
GROUP BY delivery_outcome;