import os
import pandas as pd
from datetime import datetime

def generate_report():
    print("[INFO] Loading clean datasets for report generation...")
    clean_dir = r"C:\Users\Preet\.gemini\antigravity-ide\scratch\power-bi-portfolio\data\clean"
    reports_dir = r"C:\Users\Preet\.gemini\antigravity-ide\scratch\power-bi-portfolio\reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    sales_path = os.path.join(clean_dir, "clean_sales.csv")
    cust_path = os.path.join(clean_dir, "clean_customers.csv")
    prod_path = os.path.join(clean_dir, "clean_products.csv")
    
    if not (os.path.exists(sales_path) and os.path.exists(cust_path) and os.path.exists(prod_path)):
        print("[ERROR] Clean CSV files not found. Run clean_superstore.py first.")
        return
        
    sales = pd.read_csv(sales_path)
    customers = pd.read_csv(cust_path)
    products = pd.read_csv(prod_path)
    
    # Merge datasets for comprehensive analysis
    df = sales.merge(customers, on="Customer_ID", how="left")
    df = df.merge(products, on="Product_ID", how="left")
    
    # 1. High-level Business KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    margin = (total_profit / total_sales) * 100 if total_sales > 0 else 0
    total_orders = df['Order_ID'].nunique()
    aov = total_sales / total_orders if total_orders > 0 else 0
    total_customers = df['Customer_ID'].nunique()
    
    # 2. Segment Performance
    segment_perf = df.groupby('Segment').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum')
    ).reset_index()
    segment_perf['Margin_%'] = (segment_perf['Total_Profit'] / segment_perf['Total_Sales']) * 100
    segment_perf = segment_perf.sort_values(by='Total_Sales', ascending=False)
    
    # 3. Top 5 Products by Revenue
    top_products = df.groupby('Product_Name').agg(
        Revenue=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum')
    ).reset_index().sort_values(by='Revenue', ascending=False).head(5)
    
    # 4. Regional Performance
    region_perf = df.groupby('Region').agg(
        Revenue=('Sales', 'sum'),
        Profit=('Profit', 'sum')
    ).reset_index().sort_values(by='Revenue', ascending=False)
    region_perf['Margin_%'] = (region_perf['Profit'] / region_perf['Revenue']) * 100

    report_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # --- Generate Markdown Report ---
    md_content = f"""# Superstore Daily Executive KPI Report
*Generated automatically on: {report_date}*

---

## Executive Summary KPIs
| KPI Metric | Value | Details |
| :--- | :--- | :--- |
| **Total Revenue** | ${total_sales:,.2f} | Cumulative sales across all transactions |
| **Total Profit** | ${total_profit:,.2f} | Net profit realized |
| **Profit Margin** | {margin:.2f}% | Overall profit margin ratio |
| **Total Orders** | {total_orders:,} | Unique customer orders filled |
| **Average Order Value (AOV)** | ${aov:.2f} | Average purchase value per transaction |
| **Unique Active Customers** | {total_customers:,} | Total unique customers served |

---

## Customer Segment Performance
| Segment | Revenue | Net Profit | Profit Margin |
| :--- | :--- | :--- | :--- |
"""
    for _, row in segment_perf.iterrows():
        md_content += f"| {row['Segment']} | ${row['Total_Sales']:,.2f} | ${row['Total_Profit']:,.2f} | {row['Margin_%']:.2f}% |\n"
        
    md_content += """
---

## Regional Sales Performance
| Region | Revenue | Net Profit | Profit Margin |
| :--- | :--- | :--- | :--- |
"""
    for _, row in region_perf.iterrows():
        md_content += f"| {row['Region']} | ${row['Revenue']:,.2f} | ${row['Profit']:,.2f} | {row['Margin_%']:.2f}% |\n"

    md_content += """
---

## Top 5 Revenue-Generating Products
| Product Name | Revenue | Net Profit | Units Sold |
| :--- | :--- | :--- | :--- |
"""
    for _, row in top_products.iterrows():
        # Truncate product name for clean table visual
        prod_name = row['Product_Name'][:45] + "..." if len(row['Product_Name']) > 45 else row['Product_Name']
        md_content += f"| {prod_name} | ${row['Revenue']:,.2f} | ${row['Profit']:,.2f} | {row['Quantity']:,} |\n"
        
    md_content += """
---
*End of automated pipeline report. Feed loaded successfully.*
"""
    
    # --- Generate HTML Report (Email-ready) ---
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 30px; color: #2C3E50; background-color: #F8F9FA; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        h1 {{ color: #2C3E50; border-bottom: 2px solid #3498DB; padding-bottom: 10px; margin-bottom: 5px; }}
        .timestamp {{ font-style: italic; color: #7F8C8D; margin-bottom: 25px; }}
        .kpi-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }}
        .kpi-card {{ background: #ECF0F1; padding: 20px; border-radius: 6px; text-align: center; border-left: 5px solid #3498DB; }}
        .kpi-card.profit {{ border-left-color: #2ECC71; }}
        .kpi-card.margin {{ border-left-color: #F1C40F; }}
        .kpi-title {{ font-size: 14px; text-transform: uppercase; color: #7F8C8D; font-weight: bold; margin-bottom: 5px; }}
        .kpi-value {{ font-size: 24px; font-weight: bold; color: #2C3E50; }}
        table {{ width: 100%; border-collapse: collapse; margin-bottom: 30px; }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #BDC3C7; }}
        th {{ background-color: #34495E; color: white; text-transform: uppercase; font-size: 12px; }}
        tr:nth-child(even) {{ background-color: #F2F4F4; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Superstore Daily Executive KPI Report</h1>
        <div class="timestamp">Generated automatically on: {report_date}</div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Total Revenue</div>
                <div class="kpi-value">${total_sales:,.2f}</div>
            </div>
            <div class="kpi-card profit">
                <div class="kpi-title">Net Profit</div>
                <div class="kpi-value">${total_profit:,.2f}</div>
            </div>
            <div class="kpi-card margin">
                <div class="kpi-title">Profit Margin</div>
                <div class="kpi-value">{margin:.2f}%</div>
            </div>
        </div>
        
        <h2>Customer Segment Performance</h2>
        <table>
            <thead>
                <tr>
                    <th>Segment</th>
                    <th>Revenue</th>
                    <th>Net Profit</th>
                    <th>Profit Margin</th>
                </tr>
            </thead>
            <tbody>
"""
    for _, row in segment_perf.iterrows():
        html_content += f"""                <tr>
                    <td>{row['Segment']}</td>
                    <td>${row['Total_Sales']:,.2f}</td>
                    <td>${row['Total_Profit']:,.2f}</td>
                    <td>{row['Margin_%']:.2f}%</td>
                </tr>\n"""
    html_content += """            </tbody>
        </table>
        
        <h2>Regional Sales Performance</h2>
        <table>
            <thead>
                <tr>
                    <th>Region</th>
                    <th>Revenue</th>
                    <th>Net Profit</th>
                    <th>Profit Margin</th>
                </tr>
            </thead>
            <tbody>
"""
    for _, row in region_perf.iterrows():
        html_content += f"""                <tr>
                    <td>{row['Region']}</td>
                    <td>${row['Revenue']:,.2f}</td>
                    <td>${row['Profit']:,.2f}</td>
                    <td>{row['Margin_%']:.2f}%</td>
                </tr>\n"""
    html_content += """            </tbody>
        </table>
        
        <h2>Top 5 Revenue-Generating Products</h2>
        <table>
            <thead>
                <tr>
                    <th>Product Name</th>
                    <th>Revenue</th>
                    <th>Net Profit</th>
                    <th>Units Sold</th>
                </tr>
            </thead>
            <tbody>
"""
    for _, row in top_products.iterrows():
        html_content += f"""                <tr>
                    <td>{row['Product_Name']}</td>
                    <td>${row['Revenue']:,.2f}</td>
                    <td>${row['Profit']:,.2f}</td>
                    <td>{row['Quantity']:,}</td>
                </tr>\n"""
    html_content += """            </tbody>
        </table>
    </div>
</body>
</html>
"""

    md_path = os.path.join(reports_dir, "daily_executive_report.md")
    html_path = os.path.join(reports_dir, "daily_executive_report.html")
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(md_content)
        
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"[SUCCESS] Markdown Report saved to: {md_path}")
    print(f"[SUCCESS] HTML Report saved to: {html_path}")
    print("[FINISHED] Report generation successfully executed!")

if __name__ == "__main__":
    generate_report()
