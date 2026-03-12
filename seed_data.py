# seed_data.py
import pandas as pd
from sqlalchemy import create_engine, text
import os

# 1. Replace with your Neon connection string
NEON_DATABASE_URL = "postgresql://neondb_owner:npg_MV1GnBLW7EQX@ep-restless-mud-adje84ce-pooler.c-2.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(NEON_DATABASE_URL)

def process_and_seed_month(file_path, month_name, month_str, day_columns):
    # Read the CSV (skipping the first header row as seen in your files)
    try:
        df = pd.read_excel(file_path, sheet_name=month_name, skiprows=1)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return
    
    # Clean column names to ensure matching works (uppercase and strip spaces)
    df.columns = df.columns.astype(str).str.strip().str.upper()

    # Fill NaN values in QTY, RATE, AMOUNT with 0
    df[['QTY', 'RATE', 'AMOUNT']] = df[['QTY', 'RATE', 'AMOUNT']].fillna(0)
    
    # Ensure rep exists
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO sales_reps (name, region) VALUES ('Mercy', 'Lagos Office') ON CONFLICT DO NOTHING;"))
        result = conn.execute(text("SELECT id FROM sales_reps WHERE name = 'Mercy'"))
        rep_id = result.scalar()

    # Iterate through each model
    for index, row in df.iterrows():
        # 1. Improved check to skip empty rows, "nan" strings, and subtotals
        raw_model = row['MODEL']
        if pd.isna(raw_model):
            continue
            
        model_name = str(raw_model).strip()
        if model_name.upper() == 'NAN' or model_name == '' or 'SUBTOTAL' in model_name.upper():
            continue
            
        # 2. Try to parse numbers, skip row if it contains text like 'GREEN' or 'RED'
        try:
            target_qty = float(row['QTY'])
            unit_rate = float(row['RATE'])
            target_amount = float(row['AMOUNT'])
        except ValueError:
            print(f"Skipping row due to invalid numeric data: Model={model_name}, Rate={row['RATE']}")
            continue
        
        # Calculate actuals from the final columns
        # (Using generic last two columns based on your structure: Total/Value)
        try:
            actual_qty = float(row.iloc[-2]) if pd.notna(row.iloc[-2]) else 0
            actual_amount = float(row.iloc[-1]) if pd.notna(row.iloc[-1]) else 0
        except ValueError:
            actual_qty = 0
            actual_amount = 0

        with engine.begin() as conn:
            # Insert Target
            result = conn.execute(
                text("""
                INSERT INTO monthly_targets (rep_id, month_year, model_name, target_qty, target_amount, unit_rate, actual_qty, actual_amount)
                VALUES (:rep_id, :month_year, :model_name, :target_qty, :target_amount, :unit_rate, :actual_qty, :actual_amount)
                RETURNING id;
                """),
                {"rep_id": rep_id, "month_year": month_str, "model_name": model_name, "target_qty": target_qty, "target_amount": target_amount, "unit_rate": unit_rate, "actual_qty": actual_qty, "actual_amount": actual_amount}
            )
            target_id = result.scalar()

            # Insert Daily Sales
            for day_col in day_columns:
                if day_col in df.columns and pd.notna(row[day_col]):
                    try:
                        qty_sold = float(row[day_col])
                    except ValueError:
                        continue # Skip if someone typed text in a daily column
                        
                    if qty_sold > 0:
                        # Extract day number (e.g., '10TH' -> 10, '1' -> 1)
                        day_num = int(''.join(filter(str.isdigit, day_col)))
                        date_str = f"{month_str[:-2]}{day_num:02d}"
                        
                        revenue = qty_sold * unit_rate
                        
                        conn.execute(
                            text("""
                            INSERT INTO daily_sales (target_id, sale_date, qty_sold, revenue_generated)
                            VALUES (:target_id, :sale_date, :qty_sold, :revenue)
                            """),
                            {"target_id": target_id, "sale_date": date_str, "qty_sold": qty_sold, "revenue": revenue}
                        )

print("Starting to seed database...")

def get_ordinal(n):
    if 11 <= (n % 100) <= 13:
        suffix = 'TH'
    else:
        suffix = {1: 'ST', 2: 'ND', 3: 'RD'}.get(n % 10, 'TH')
    return f"{n}{suffix}"

# Month mappings based on the columns generated earlier
jan_cols = ['2ND', '3RD', '4TH', '5TH', '6TH', '7TH', '9TH', '10TH', '11TH', '12TH', '13TH', '14TH', '16TH', '17TH', '18TH', '19TH', '20TH', '21ST', '22ND', '24TH', '25TH', '26TH', '27TH', '28TH', '30TH', '31ST']
feb_cols = ['10TH', '11TH', '12TH', '13TH', '14TH', '15TH', '16TH', '17TH', '18TH', '19TH', '20TH', '21ST', '22ND', '24TH', '25TH', '26TH', '27TH', '28TH']
mar_cols = [get_ordinal(i) for i in range(1, 32)]

# process_and_seed_month("MERCY'S SALE PLAN.xlsx - JAN.csv", "2026-01-01", jan_cols)
# process_and_seed_month("MERCY'S SALE PLAN.xlsx - FEB.csv", "2026-02-01", feb_cols)
# process_and_seed_month("MERCY'S SALE PLAN.xlsx - MAR.csv", "2026-03-01", mar_cols)

print("Seeding complete!")

if __name__ == "__main__":
    process_and_seed_month("MERCY'S SALE PLAN.xlsx", "JAN", "2026-01-01", jan_cols)
    process_and_seed_month("MERCY'S SALE PLAN.xlsx", "FEB", "2026-02-01", feb_cols)
    process_and_seed_month("MERCY'S SALE PLAN.xlsx", "MAR", "2026-03-01", mar_cols)