-- ==============================================================================
-- 📂 CASE STUDY 2: SUBSCRIPTION CHURN & RETENTION ANALYSIS
-- ==============================================================================

-- 🔍 PROBLEM STATEMENT:
-- Customer retention is the key to SaaS and retail business profitability.
-- In this case study, we analyze customer lifetime activity, identify the churn point,
-- group users by acquisition cohorts, and calculate rolling 30-day customer churn rates.

-- ------------------------------------------------------------------------------
-- Task 1: Find the Average Customer Lifespan (Days between first and last purchase).
-- ------------------------------------------------------------------------------
WITH customer_lifespans AS (
    SELECT 
        customer_id,
        MIN(order_date::date) AS first_purchase,
        MAX(order_date::date) AS last_purchase,
        (MAX(order_date::date) - MIN(order_date::date)) AS lifespan_days
    FROM sales
    GROUP BY customer_id
)
SELECT 
    ROUND(AVG(lifespan_days), 1) AS average_lifespan_days,
    MIN(lifespan_days) AS shortest_lifespan,
    MAX(lifespan_days) AS longest_lifespan
FROM customer_lifespans
WHERE lifespan_days > 0; -- Excludes one-time buyers

-- 💡 Insight: An average customer lifespan of ~1,000 days is strong, but focus should be on 
-- conversion techniques for one-time buyers (lifespan = 0 days) who represent a significant cost.


-- ------------------------------------------------------------------------------
-- Task 2: Calculate Month-over-Month Churn Rates.
-- ------------------------------------------------------------------------------
WITH monthly_active_users AS (
    SELECT DISTINCT
        customer_id,
        DATE_TRUNC('month', order_date::date) AS active_month
    FROM sales
),
churn_analysis AS (
    SELECT 
        m1.active_month,
        COUNT(DISTINCT m1.customer_id) AS active_this_month,
        COUNT(DISTINCT m2.customer_id) AS retained_next_month
    FROM monthly_active_users m1
    LEFT JOIN monthly_active_users m2 
        ON m1.customer_id = m2.customer_id 
        AND m2.active_month = m1.active_month + INTERVAL '1 month'
    GROUP BY m1.active_month
)
SELECT 
    active_month,
    active_this_month,
    retained_next_month,
    (active_this_month - retained_next_month) AS churned_customers,
    ROUND(((active_this_month - retained_next_month)::numeric / active_this_month * 100), 2) AS monthly_churn_rate_pct
FROM churn_analysis
ORDER BY active_month;

-- 💡 Insight: Identifies operational churn trends. A sudden spike in churn rate on certain 
-- months indicates post-holiday slumps or uncompetitive promotional activities.


-- ------------------------------------------------------------------------------
-- Task 3: Identify VIP customers at risk of churning.
-- (Defined as: Lifetime spent > $5,000, last purchase was > 180 days ago).
-- ------------------------------------------------------------------------------
WITH customer_stats AS (
    SELECT 
        customer_id,
        SUM(sales) AS total_spend,
        MAX(order_date::date) AS last_order
    FROM sales
    GROUP BY customer_id
)
SELECT 
    customer_id,
    ROUND(total_spend::numeric, 2) AS lifetime_spend,
    last_order,
    ('2018-01-01'::date - last_order) AS days_since_last_purchase -- Using 2018-01-01 as the benchmark snapshot date
FROM customer_stats
WHERE ('2018-01-01'::date - last_order) > 180
  AND total_spend > 5000
ORDER BY lifetime_spend DESC;

-- 💡 Insight: Generate customer-specific lists for sales accounts to contact with exclusive,
-- high-value reactivation campaigns before the relationship is permanently lost.
