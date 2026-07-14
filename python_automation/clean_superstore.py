import os
import pandas as pd

def clean_sales(raw_path, output_dir):
    print("[INFO] Cleaning Sales Data...")
    df = pd.read_csv(raw_path, encoding='utf-8')
    
    # 1. Clean Column Names (replace spaces with underscores, strip whitespace)
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # 2. Handle Data Types
    df['Order_Date'] = pd.to_datetime(df['Order_Date']).dt.strftime('%Y-%m-%d')
    df['Ship_Date'] = pd.to_datetime(df['Ship_Date']).dt.strftime('%Y-%m-%d')
    df['Sales'] = df['Sales'].astype(float).round(2)
    df['Quantity'] = df['Quantity'].astype(int)
    df['Discount'] = df['Discount'].astype(float).round(4)
    df['Profit'] = df['Profit'].astype(float).round(4)
    
    # 3. Drop rows with null key identifiers if any
    df = df.dropna(subset=['Order_ID', 'Customer_ID', 'Product_ID'])
    
    # Save output
    output_path = os.path.join(output_dir, 'clean_sales.csv')
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Sales Data Cleaned! Output saved to: {output_path} (Shape: {df.shape})")

def clean_customer(raw_path, output_dir):
    print("[INFO] Cleaning Customer Data...")
    df = pd.read_csv(raw_path, encoding='latin1')
    
    # 1. Clean Column Names
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # 2. Standardize Strings (Trim whitespaces, capitalize names)
    df['Customer_Name'] = df['Customer_Name'].str.strip().str.title()
    df['Segment'] = df['Segment'].str.strip()
    df['City'] = df['City'].str.strip()
    df['State'] = df['State'].str.strip()
    
    # 3. Fix ZIP codes (zero-pad to 5 characters, convert float representation to text)
    df['Postal_Code'] = df['Postal_Code'].astype(int).astype(str).str.zfill(5)
    
    # 4. Fill missing Age values with the median age
    median_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(median_age).astype(int)
    
    # Save output
    output_path = os.path.join(output_dir, 'clean_customers.csv')
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Customer Data Cleaned! Output saved to: {output_path} (Shape: {df.shape})")

def clean_product(raw_path, output_dir):
    print("[INFO] Cleaning Product Data...")
    df = pd.read_csv(raw_path, encoding='utf-8')
    
    # 1. Clean Column Names
    df.columns = df.columns.str.strip().str.replace(' ', '_')
    
    # 2. Trim string values
    df['Category'] = df['Category'].str.strip()
    df['Sub_Category'] = df['Sub-Category'].str.strip() if 'Sub-Category' in df.columns else df['Sub_Category'].str.strip()
    df['Product_Name'] = df['Product_Name'].str.strip()
    
    # Drop old 'Sub-Category' if duplicated due to rename
    if 'Sub-Category' in df.columns:
        df = df.drop(columns=['Sub-Category'])
        
    # Remove duplicate products to maintain reference integrity
    df = df.drop_duplicates(subset=['Product_ID'])
    
    # Save output
    output_path = os.path.join(output_dir, 'clean_products.csv')
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Product Data Cleaned! Output saved to: {output_path} (Shape: {df.shape})")

if __name__ == "__main__":
    raw_dir = r"D:\Tableau resources"
    output_dir = r"C:\Users\Preet\.gemini\antigravity-ide\scratch\power-bi-portfolio\data\clean"
    
    os.makedirs(output_dir, exist_ok=True)
    
    sales_file = os.path.join(raw_dir, "Sales.csv")
    customer_file = os.path.join(raw_dir, "Customer.csv")
    product_file = os.path.join(raw_dir, "Product.csv")
    
    if os.path.exists(sales_file):
        clean_sales(sales_file, output_dir)
    else:
        print(f"[ERROR] Could not find Sales file at: {sales_file}")
        
    if os.path.exists(customer_file):
        clean_customer(customer_file, output_dir)
    else:
        print(f"[ERROR] Could not find Customer file at: {customer_file}")
        
    if os.path.exists(product_file):
        clean_product(product_file, output_dir)
    else:
        print(f"[ERROR] Could not find Product file at: {product_file}")
        
    print("\n[FINISHED] ETL Process complete! Clean data is ready for Power BI loading.")
