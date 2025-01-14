import sqlite3
from typing import List, Dict
from tabulate import tabulate  # pip install tabulate

def inspect_sqlite_db(db_path: str = "products.db"):
    """Inspect SQLite database structure and content"""
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n=== Database Tables ===")
    for (table_name,) in tables:
        print(f"\n--- Table: {table_name} ---")
        
        # Get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        # Print columns info
        columns_info = []
        for col in columns:
            cid, name, type_, notnull, default, pk = col
            columns_info.append([name, type_, "NOT NULL" if notnull else "", "PK" if pk else ""])
        
        print("\nColumns:")
        print(tabulate(columns_info, headers=["Name", "Type", "Null", "Key"], tablefmt="grid"))
        
        # Get sample data
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1;")
        sample = cursor.fetchone()
        
        if sample:
            print("\nSample row:")
            sample_data = []
            for col, val in zip([col[1] for col in columns], sample):
                sample_data.append([col, val])
            print(tabulate(sample_data, headers=["Column", "Value"], tablefmt="grid"))
        else:
            print("\nNo data in table")
            
    conn.close()

if __name__ == "__main__":
    try:
        inspect_sqlite_db()
    except sqlite3.OperationalError as e:
        print(f"Error accessing database: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
