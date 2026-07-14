import os
import json
import pandas as pd

def generate_assets():
    print("[INFO] Processing clean data for the interactive dashboard...")
    clean_dir = r"C:\Users\Preet\.gemini\antigravity-ide\scratch\power-bi-portfolio\data\clean"
    output_dir = r"C:\Users\Preet\.gemini\antigravity-ide\scratch\power-bi-portfolio\dashboard_preview"
    os.makedirs(output_dir, exist_ok=True)
    
    sales_path = os.path.join(clean_dir, "clean_sales.csv")
    cust_path = os.path.join(clean_dir, "clean_customers.csv")
    prod_path = os.path.join(clean_dir, "clean_products.csv")
    
    if not (os.path.exists(sales_path) and os.path.exists(cust_path) and os.path.exists(prod_path)):
        print("[ERROR] Clean CSV files not found. Run clean_superstore.py first.")
        return
        
    sales = pd.read_csv(sales_path)
    customers = pd.read_csv(cust_path)
    products = pd.read_csv(prod_path)
    
    # Merge datasets
    df = sales.merge(customers, on="Customer_ID", how="left")
    df = df.merge(products, on="Product_ID", how="left")
    
    # Standardize dates
    df['Year'] = pd.to_datetime(df['Order_Date']).dt.year
    df['Month'] = pd.to_datetime(df['Order_Date']).dt.strftime('%b')
    df['MonthNum'] = pd.to_datetime(df['Order_Date']).dt.month
    
    # 1. Total Metrics
    metrics = {
        "sales": float(df['Sales'].sum()),
        "profit": float(df['Profit'].sum()),
        "orders": int(df['Order_ID'].nunique()),
        "customers": int(df['Customer_ID'].nunique())
    }
    
    # 2. Monthly Trend (Grouped by Year, MonthNum, Month)
    trend = df.groupby(['Year', 'MonthNum', 'Month']).agg(
        sales=('Sales', 'sum'),
        profit=('Profit', 'sum')
    ).reset_index().sort_values(by=['Year', 'MonthNum'])
    
    trend_list = []
    for _, r in trend.iterrows():
        trend_list.append({
            "year": int(r['Year']),
            "monthNum": int(r['MonthNum']),
            "month": str(r['Month']),
            "sales": float(r['sales']),
            "profit": float(r['profit'])
        })
        
    # 3. Category & Segment Matrix
    matrix = df.groupby(['Year', 'Category', 'Segment']).agg(
        sales=('Sales', 'sum'),
        profit=('Profit', 'sum')
    ).reset_index()
    
    matrix_list = []
    for _, r in matrix.iterrows():
        matrix_list.append({
            "year": int(r['Year']),
            "category": str(r['Category']),
            "segment": str(r['Segment']),
            "sales": float(r['sales']),
            "profit": float(r['profit'])
        })
        
    # 4. Top Sub-Categories
    subcat = df.groupby(['Year', 'Category', 'Sub_Category']).agg(
        sales=('Sales', 'sum'),
        profit=('Profit', 'sum')
    ).reset_index().sort_values(by='sales', ascending=False)
    
    subcat_list = []
    for _, r in subcat.iterrows():
        subcat_list.append({
            "year": int(r['Year']),
            "category": str(r['Category']),
            "subCategory": str(r['Sub_Category']),
            "sales": float(r['sales']),
            "profit": float(r['profit'])
        })
        
    # 5. Regional & State Performance (with some lat-long approximations for mapping)
    state_coords = {
        "California": [36.7783, -119.4179],
        "New York": [40.7128, -74.0060],
        "Texas": [31.9686, -99.9018],
        "Florida": [27.6648, -81.5158],
        "Washington": [47.7511, -120.7401],
        "Pennsylvania": [41.2033, -77.1945],
        "Illinois": [40.6331, -89.3985],
        "Ohio": [40.4173, -82.9071],
        "North Carolina": [35.7596, -79.0193],
        "Michigan": [44.3148, -85.6024],
        "Virginia": [37.4316, -78.6569],
        "Georgia": [32.1656, -82.9001],
        "Indiana": [40.2672, -86.1349],
        "Colorado": [39.5501, -105.7821],
        "Arizona": [34.0489, -111.0937],
        "Tennessee": [35.5175, -86.5804],
        "Minnesota": [46.7296, -94.6859],
        "Massachusetts": [42.4072, -71.3824],
        "Kentucky": [37.8393, -84.2700],
        "Wisconsin": [43.7844, -88.7879],
        "Oregon": [43.8041, -120.5542],
        "Maryland": [39.0458, -76.6413],
        "Delaware": [38.9108, -75.5277],
        "New Jersey": [40.0583, -74.4057]
    }
    
    state_perf = df.groupby(['Year', 'State', 'Region']).agg(
        sales=('Sales', 'sum'),
        profit=('Profit', 'sum')
    ).reset_index()
    
    state_list = []
    for _, r in state_perf.iterrows():
        name = r['State']
        coords = state_coords.get(name, [37.0902, -95.7129]) # fallback to center of US
        state_list.append({
            "year": int(r['Year']),
            "state": str(name),
            "region": str(r['Region']),
            "sales": float(r['sales']),
            "profit": float(r['profit']),
            "lat": coords[0],
            "lng": coords[1]
        })
        
    # Write JSON data to js file
    data_js_path = os.path.join(output_dir, "dashboard_data.js")
    with open(data_js_path, "w", encoding="utf-8") as f:
        f.write("const dashboardData = ")
        json.dump({
            "summary": metrics,
            "trend": trend_list,
            "matrix": matrix_list,
            "subcat": subcat_list,
            "states": state_list
        }, f, indent=2)
        f.write(";")
        
    print(f"[SUCCESS] Dashboard assets data file created: {data_js_path}")

if __name__ == "__main__":
    generate_assets()
