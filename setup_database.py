import sqlite3
import pandas as pd

# Load dataset
data = pd.read_csv("data/cleaned_amazon_products_dataset.csv")

# Connect to SQLite database
conn = sqlite3.connect(
    "data/products.db"
)  # Database will be created in the 'data' folder
cursor = conn.cursor()

# Create table (adjust column names and types based on your dataset)
data.to_sql("products", conn, if_exists="replace", index=False)

print("Database and table created successfully!")
conn.close()
