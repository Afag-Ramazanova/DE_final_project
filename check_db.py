import mysql.connector

connection = None  # Define connection variable outside the try block

try:
    # Attempt to connect to the database
    connection = mysql.connector.connect(
        host="inventorycheck.cnwm886wwadv.us-east-1.rds.amazonaws.com",
        user="admin",
        password="afaglucy101",
    )

    if connection.is_connected():
        print(connection)
        print("Successfully connected to the database.")

        # Create a cursor to execute SQL queries
        cursor = connection.cursor()

        # Query to show all tables
        cursor.execute("SHOW DATABASES;")
        tables = cursor.fetchall()

        print("Available tables:")
        for table in tables:
            print(table[0])

except mysql.connector.Error as err:
    print(f"Error: {err}")

finally:
    if connection and connection.is_connected():
        connection.close()
        print("Database connection closed.")
