-- ============================================================
-- Analytics & Reporting Queries
-- ============================================================

-- 1. Top-selling menu items overall
SELECT
    mi.name          AS item,
    mi.category,
    SUM(oi.quantity) AS total_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM Order_Item oi
JOIN Menu_Item mi ON oi.item_id = mi.item_id
GROUP BY mi.item_id, mi.name, mi.category
ORDER BY total_sold DESC
LIMIT 10;

-- 2. Revenue per branch
SELECT
    b.name           AS branch,
    b.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.amount)    AS total_revenue
FROM Branch b
JOIN `Order` o  ON b.branch_id = o.branch_id
JOIN Payment p  ON o.order_id  = p.order_id
WHERE p.status = 'Paid'
GROUP BY b.branch_id, b.name, b.city
ORDER BY total_revenue DESC;

-- 3. Average rating per branch
SELECT
    b.name  AS branch,
    b.city,
    ROUND(AVG(r.rating), 2) AS avg_rating,
    COUNT(r.review_id)      AS total_reviews
FROM Branch b
JOIN Review r ON b.branch_id = r.branch_id
GROUP BY b.branch_id, b.name, b.city
ORDER BY avg_rating DESC;

-- 4. Low inventory alerts (below reorder level)
SELECT
    b.name       AS branch,
    i.ingredient,
    i.quantity,
    i.unit,
    i.reorder_level
FROM Inventory i
JOIN Branch b ON i.branch_id = b.branch_id
WHERE i.quantity <= i.reorder_level
ORDER BY b.name, i.ingredient;

-- 5. Customer order history
SELECT
    c.name          AS customer,
    b.name          AS branch,
    o.order_id,
    o.order_type,
    o.status,
    p.amount,
    p.method,
    o.ordered_at
FROM Customer c
JOIN `Order` o  ON c.customer_id = o.customer_id
JOIN Branch b   ON o.branch_id   = b.branch_id
LEFT JOIN Payment p ON o.order_id = p.order_id
ORDER BY o.ordered_at DESC;

-- 6. Orders by status per branch
SELECT
    b.name        AS branch,
    o.status,
    COUNT(*)      AS count
FROM `Order` o
JOIN Branch b ON o.branch_id = b.branch_id
GROUP BY b.branch_id, b.name, o.status
ORDER BY b.name, o.status;

-- 7. Most valuable customers
SELECT
    c.name,
    c.city,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(p.amount)              AS total_spent
FROM Customer c
JOIN `Order` o  ON c.customer_id = o.customer_id
JOIN Payment p  ON o.order_id    = p.order_id
WHERE p.status = 'Paid'
GROUP BY c.customer_id, c.name, c.city
ORDER BY total_spent DESC;

-- 8. Revenue by payment method
SELECT
    method,
    COUNT(*) AS transactions,
    SUM(amount) AS total
FROM Payment
WHERE status = 'Paid'
GROUP BY method
ORDER BY total DESC;
