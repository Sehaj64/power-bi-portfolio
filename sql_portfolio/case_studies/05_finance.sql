-- ==============================================================================
-- 📂 CASE STUDY 5: CORPORATE FINANCE, BUDGETING & WORKING CAPITAL
-- ==============================================================================

-- 🔍 PROBLEM STATEMENT:
-- Financial analysts need to evaluate department expenses, monitor budget variances, 
-- and calculate accounts receivable aging metrics to manage working capital.
-- (This case study references an enterprise financial database schema: transactions, accounts, budgets).

-- ------------------------------------------------------------------------------
-- Task 1: Calculate Budget Variance (Actual Expenditures vs. Allocated Budget).
-- ------------------------------------------------------------------------------
SELECT 
    b.cost_center,
    b.fiscal_year,
    ROUND(b.allocated_amount::numeric, 2) AS budget_allocated,
    ROUND(SUM(t.amount)::numeric, 2) AS actual_spent,
    ROUND((SUM(t.amount) - b.allocated_amount)::numeric, 2) AS budget_variance,
    ROUND(((SUM(t.amount) - b.allocated_amount) / b.allocated_amount * 100)::numeric, 2) AS variance_percent
FROM budgets b
LEFT JOIN transactions t 
    ON b.department_id = t.department_id 
    AND t.transaction_type = 'Expense'
    AND EXTRACT(YEAR FROM t.transaction_date) = b.fiscal_year
GROUP BY b.cost_center, b.fiscal_year, b.allocated_amount
ORDER BY variance_percent DESC;

-- 💡 Insight: Highlights cost centers that are over budget. Positive variance represents cost
-- overruns that require immediate review, while negative variance highlights savings.


-- ------------------------------------------------------------------------------
-- Task 2: Calculate Accounts Receivable (AR) Aging buckets and risk analysis.
-- ------------------------------------------------------------------------------
WITH invoice_aging AS (
    SELECT 
        customer_id,
        invoice_id,
        invoice_amount,
        due_date,
        payment_date,
        CASE 
            WHEN payment_date IS NULL THEN ('2018-01-01'::date - due_date::date) -- snapshot date
            ELSE (payment_date::date - due_date::date)
        END AS days_overdue
    FROM invoices
    WHERE payment_status = 'Unpaid' OR payment_date > due_date
)
SELECT 
    CASE 
        WHEN days_overdue <= 0 THEN '01. Current (On Time)'
        WHEN days_overdue BETWEEN 1 AND 30 THEN '02. 1-30 Days Overdue'
        WHEN days_overdue BETWEEN 31 AND 90 THEN '03. 31-90 Days Overdue'
        ELSE '04. Write-off Risk (>90 Days Overdue)'
    END AS aging_bucket,
    COUNT(invoice_id) AS invoice_count,
    ROUND(SUM(invoice_amount)::numeric, 2) AS total_receivables,
    ROUND((SUM(invoice_amount) / SUM(SUM(invoice_amount)) OVER () * 100)::numeric, 2) AS allocation_percent
FROM invoice_aging
GROUP BY aging_bucket
ORDER BY aging_bucket;

-- 💡 Insight: Standard cash-flow tracking metric. High balances in the '>90 Days' bucket
-- indicate bad debt risks, requiring collection agency escalation.


-- ------------------------------------------------------------------------------
-- Task 3: Calculate EBITDA (Earnings Before Interest, Taxes, Depreciation, and Amortization).
-- ------------------------------------------------------------------------------
WITH financial_ledger AS (
    SELECT 
        account_category,
        SUM(amount) AS net_amount
    FROM general_ledger
    WHERE fiscal_year = 2017
    GROUP BY account_category
)
SELECT 
    ROUND(SUM(CASE WHEN account_category = 'Revenue' THEN net_amount ELSE 0 END)::numeric, 2) AS revenue,
    ROUND(SUM(CASE WHEN account_category = 'COGS' THEN -net_amount ELSE 0 END)::numeric, 2) AS cost_of_goods_sold,
    ROUND(SUM(CASE WHEN account_category = 'Operating_Expense' THEN -net_amount ELSE 0 END)::numeric, 2) AS opex,
    ROUND((
        SUM(CASE WHEN account_category = 'Revenue' THEN net_amount ELSE 0 END) - 
        SUM(CASE WHEN account_category = 'COGS' THEN net_amount ELSE 0 END) - 
        SUM(CASE WHEN account_category = 'Operating_Expense' THEN net_amount ELSE 0 END)
    )::numeric, 2) AS ebitda
FROM financial_ledger;

-- 💡 Insight: Primary metric for business valuation and profitability. It isolates operational
-- performance from financing, accounting policy, and tax effects.
