import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

def import_csv_to_db(csv_file_path: str, table_name: str):
    """
    Reads a CSV file and uploads it to CockroachDB.
    """
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ ERROR: DATABASE_URL not found in .env")
        return

    try:
        # 1. Connect to the database
        engine = create_engine(db_url)
        print(f"Connecting to database...")

        # 2. Read the CSV using pandas
        print(f"Reading CSV file: {csv_file_path}...")
        df = pd.read_csv(csv_file_path)
        
        # 3. Upload to database
        # if_exists='replace' will drop the table if it exists and recreate it.
        # Use if_exists='append' if you want to add to an existing table.
        print(f"Uploading {len(df)} rows to table '{table_name}'...")
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"✅ SUCCESS: Data successfully uploaded to '{table_name}'!")
        
    except Exception as e:
        print(f"❌ ERROR: Failed to import CSV.")
        print(f"Details: {e}")

if __name__ == "__main__":
    # --- INSTRUCTIONS ---
    # 1. Place your CSV file in the same folder as this script, or provide the full path.
    # 2. Update the variables below:
    
    CSV_FILE_NAME = "sample_company_sales_2025_100k.csv"   # <-- CHANGE THIS to your actual CSV filename
    TABLE_NAME = "sales_data"           # <-- CHANGE THIS to what you want the table to be named in the DB
    
    if os.path.exists(CSV_FILE_NAME):
        import_csv_to_db(CSV_FILE_NAME, TABLE_NAME)
    else:
        print(f"⚠️ Could not find '{CSV_FILE_NAME}'. Please make sure the file exists and the path is correct.")
