import mysql.connector
import csv
from dotenv import load_dotenv
import os

load_dotenv()
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)

cursor = connection.cursor()

# Load data from CSV file
with open('data/cleaned_amazon_products_dataset.csv', mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        cursor.execute("""
            INSERT INTO items (name, main_category, sub_category, ratings, no_of_ratings, discount_price, actual_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, row)

connection.commit()
cursor.close()
connection.close()

print("Data loaded successfully!")
