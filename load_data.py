import mysql.connector
import csv
from dotenv import load_dotenv
import os




# Load environment variables
load_dotenv()

# Connect to the database
connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

cursor = connection.cursor()

# Load data from CSV file
batch_size = 1000  # Adjust batch size for efficiency
data_batch = []

with open(
    "data/cleaned_amazon_products_dataset.csv", mode="r", encoding="utf-8"
) as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row

    for row in csv_reader:
        data_batch.append(row)
        if len(data_batch) == batch_size:
            cursor.executemany(
                """
                INSERT INTO items (name, main_category, sub_category, ratings, no_of_ratings, discount_price, actual_price)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
                data_batch,
            )
            connection.commit()
            data_batch = []

    if data_batch:
        cursor.executemany(
            """
            INSERT INTO items (name, main_category, sub_category, ratings, no_of_ratings, discount_price, actual_price)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """,
            data_batch,
        )
        connection.commit()

cursor.close()
connection.close()

print("Data loaded successfully!")
