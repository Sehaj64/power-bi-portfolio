-- ==============================================================================
-- 📂 CASE STUDY 1: SALES PERFORMANCE & GEOGRAPHIC EXPANSION
-- ==============================================================================

-- 🔍 PROBLEM STATEMENT:
-- The regional vice president wants to evaluate sales performance across different states.
-- We need to identify underperforming states, track monthly sales targets, evaluate the
-- impact of product discounts on profit margins, and list the top 3 sub-categories per region.

-- ------------------------------------------------------------------------------
-- Task 1: Identify underperforming states where the profit margin is negative.
-- ------------------------------------------------------------------------------
WITH state_performance AS (
    SELECT 
        c.state,
        ROUND(SUM(s.sales)::numeric, 2) AS revenue,
        ROUND(SUM(s.profit)::numeric, 2) AS profit,
        ROUND((SUM(s.profit) / SUM(s.sales) * 100)::numeric, 2) AS margin_percent
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    GROUP BY c.state
)
SELECT * 
FROM state_performance
WHERE profit < 0
ORDER BY profit ASC;

-- 💡 Insight: Highlight states like Texas, Ohio, and Illinois. Although they generate high revenue, 
-- they are unprofitable due to heavy localized discount structures (e.g. up to 80% on binders/furniture).


-- ------------------------------------------------------------------------------
-- Task 2: Calculate Month-over-Month (MoM) sales velocity and growth rates.
-- ------------------------------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        DATE_TRUNC('month', order_date::date) AS order_month,
        SUM(sales) AS revenue
    FROM sales
    GROUP BY order_month
)
SELECT 
    order_month,
    ROUND(revenue::numeric, 2) AS current_month_sales,
    ROUND(LAG(revenue) OVER (ORDER BY order_month)::numeric, 2) AS prior_month_sales,
    ROUND((revenue - LAG(revenue) OVER (ORDER BY order_month))::numeric, 2) AS change,
    ROUND(((revenue - LAG(revenue) OVER (ORDER BY order_month)) / LAG(revenue) OVER (ORDER BY order_month) * 100)::numeric, 2) AS growth_rate_pct
FROM monthly_metrics
ORDER BY order_month;

-- 💡 Insight: Demonstrates high seasonal volatility. Visualizing this trend in Power BI explains why 
-- warehouse capacity is strained in Q4 (due to holiday shopping) but experiences dry spells in Q1.


-- ------------------------------------------------------------------------------
-- Task 3: Identify Top 3 profit-generating sub-categories within each geographic region.
-- ------------------------------------------------------------------------------
WITH regional_sub_profits AS (
    SELECT 
        c.region,
        p.sub_category,
        SUM(s.profit) AS total_profit,
        DENSE_RANK() OVER (PARTITION BY c.region ORDER BY SUM(s.profit) DESC) AS rank
    FROM sales s
    JOIN customers c ON s.customer_id = c.customer_id
    JOIN products p ON s.product_id = p.product_id
    GROUP BY c.region, p.sub_category
)
SELECT 
    region,
    sub_category,
    ROUND(total_profit::numeric, 2) AS net_profit
FROM regional_sub_profits
WHERE rank <= 3
ORDER BY region, net_profit DESC;

-- 💡 Insight: Copiers and Phones are consistently in the top 3 across all regions, confirming 
-- that corporate technology products are the primary margin drivers of the business.
