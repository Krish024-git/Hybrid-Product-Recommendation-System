import os
import sqlite3
import pandas as pd

# Define paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(DATA_DIR, "recommendation_system.db")

PRODUCTS_CSV = os.path.join(DATA_DIR, "products.csv")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
RATINGS_CSV = os.path.join(DATA_DIR, "ratings.csv")

def setup_database():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 1. Create Tables
    print("Creating tables...")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        product_id TEXT PRIMARY KEY,
        product_name TEXT NOT NULL,
        brand TEXT,
        category TEXT,
        description TEXT,
        price REAL,
        rating REAL,
        image_path TEXT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        age INTEGER,
        gender TEXT,
        location TEXT
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ratings (
        user_id INTEGER,
        product_id TEXT,
        rating REAL,
        PRIMARY KEY (user_id, product_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS recommendation_history (
        history_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        product_id TEXT,
        recommendation_type TEXT,
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (product_id) REFERENCES products(product_id)
    );
    """)
    
    # Commit table creation
    conn.commit()
    
    # 2. Ingest Data from CSV files
    print("Ingesting data from CSV files...")
    
    # Products
    if os.path.exists(PRODUCTS_CSV):
        df_prod = pd.read_csv(PRODUCTS_CSV)
        # Rename columns to match db schema if necessary
        df_prod.columns = ["product_id", "product_name", "brand", "category", "description", "price", "rating", "image_path"]
        df_prod.to_sql("products", conn, if_exists="replace", index=False)
        # Re-apply PRIMARY KEY constraints in SQLite by recreating table if using 'replace'
        # But Pandas replace drops constraints. It's fine for SQLite if we query it, but let's do it cleanly:
        # Better: clear table and insert using to_sql with append, or just keep default pandas behavior.
        # Let's keep it simple: truncate and append to preserve schemas or let pandas create them, 
        # but to ensure primary keys are correct, we can clear the table and use method='multi' to insert.
        cursor.execute("DELETE FROM products;")
        df_prod.to_sql("products", conn, if_exists="append", index=False)
        print(f"Products table populated with {len(df_prod)} records.")
    else:
        print(f"Error: {PRODUCTS_CSV} not found!")

    # Users
    if os.path.exists(USERS_CSV):
        df_users = pd.read_csv(USERS_CSV)
        df_users.columns = ["user_id", "age", "gender", "location"]
        cursor.execute("DELETE FROM users;")
        df_users.to_sql("users", conn, if_exists="append", index=False)
        print(f"Users table populated with {len(df_users)} records.")
    else:
        print(f"Error: {USERS_CSV} not found!")

    # Ratings
    if os.path.exists(RATINGS_CSV):
        df_ratings = pd.read_csv(RATINGS_CSV)
        df_ratings.columns = ["user_id", "product_id", "rating"]
        cursor.execute("DELETE FROM ratings;")
        df_ratings.to_sql("ratings", conn, if_exists="append", index=False)
        print(f"Ratings table populated with {len(df_ratings)} records.")
    else:
        print(f"Error: {RATINGS_CSV} not found!")
        
    conn.commit()
    conn.close()
    print("Database setup successfully completed!")

if __name__ == "__main__":
    setup_database()
