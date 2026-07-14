-- ==============================================================================
-- 📂 CASE STUDY 3: HR COMPENSATIONS & DEPARTAMENTAL TURNOVER
-- ==============================================================================

-- 🔍 PROBLEM STATEMENT:
-- HR leadership is analyzing organizational health, department salaries, and retention.
-- We must identify salary discrepancies across departments, calculate company attrition
-- rates, and find high-performing employees who are under-compensated.
-- (This case study references a standard enterprise HR schema: employees, departments, evaluations).

-- ------------------------------------------------------------------------------
-- Task 1: Find departmental salary averages, ranges, and standard deviations.
-- ------------------------------------------------------------------------------
SELECT 
    d.department_name,
    COUNT(e.employee_id) AS total_employees,
    ROUND(AVG(e.salary)::numeric, 2) AS average_salary,
    MIN(e.salary) AS min_salary,
    MAX(e.salary) AS max_salary,
    ROUND(STDDEV(e.salary)::numeric, 2) AS salary_variance
FROM employees e
JOIN departments d ON e.department_id = d.department_id
GROUP BY d.department_name
ORDER BY average_salary DESC;

-- 💡 Insight: Highlight pay disparities across business units. High salary variances inside a 
-- department might point to unfair pay distribution or a high concentration of senior executives.


-- ------------------------------------------------------------------------------
-- Task 2: Calculate attrition rate by tenure (employees leaving within their first year).
-- ------------------------------------------------------------------------------
WITH staff_tenure AS (
    SELECT 
        employee_id,
        hire_date,
        termination_date,
        CASE WHEN termination_date IS NOT NULL THEN 1 ELSE 0 END AS left_company,
        (termination_date::date - hire_date::date) / 365.0 AS tenure_years
    FROM employees
)
SELECT 
    CASE 
        WHEN tenure_years < 1.0 THEN 'New Hire (<1 Year)'
        WHEN tenure_years BETWEEN 1.0 AND 3.0 THEN 'Mid-Level (1-3 Years)'
        ELSE 'Senior (3+ Years / Active)'
    END AS employee_tenure_tier,
    COUNT(employee_id) AS employee_count,
    SUM(left_company) AS departed_count,
    ROUND((SUM(left_company)::numeric / COUNT(employee_id) * 100), 2) AS attrition_rate_percent
FROM staff_tenure
GROUP BY employee_tenure_tier;

-- 💡 Insight: If the attrition rate for 'New Hires (<1 Year)' is high, it flags major issues 
-- in candidate sourcing, onboarding processes, or unmet expectations in the recruitment phase.


-- ------------------------------------------------------------------------------
-- Task 3: Identify high-performing, under-paid employees (Potential Attrition Risks).
-- (Criteria: Performance score > 4.5/5.0, Salary is below the 40th percentile of their department).
-- ------------------------------------------------------------------------------
WITH department_salary_distribution AS (
    SELECT 
        employee_id,
        first_name || ' ' || last_name AS employee_name,
        department_id,
        salary,
        performance_rating,
        PERCENT_RANK() OVER (PARTITION BY department_id ORDER BY salary) AS salary_percentile
    FROM employees
)
SELECT 
    d.department_name,
    sd.employee_name,
    sd.salary,
    sd.performance_rating,
    ROUND((sd.salary_percentile * 100)::numeric, 1) AS department_salary_percentile
FROM department_salary_distribution sd
JOIN departments d ON sd.department_id = d.department_id
WHERE sd.performance_rating >= 4.5
  AND sd.salary_percentile < 0.40
ORDER BY sd.performance_rating DESC, sd.salary ASC;

-- 💡 Insight: Actionable talent preservation list. Retaining these high-performing, under-compensated
-- employees is critical, and they should be prioritized for immediate salary adjustments.
