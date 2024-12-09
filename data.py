import sqlite3


def process_message(message):
    # Connect to the SQLite database using a context manager
    try:
        with sqlite3.connect("data/products.db") as conn:
            cursor = conn.cursor()

            # If the message contains an SQL query (e.g., SELECT * FROM ...)
            if message.strip().upper().startswith("SELECT"):
                try:
                    # Execute the query
                    cursor.execute(message)
                    result = cursor.fetchone()  # Fetch the first row
                    if result:
                        return f"{result}"  # Return the result as a string
                    else:
                        return "No results found."
                except sqlite3.Error as e:
                    return f"SQL error: {e}"
            else:
                return f"Message received: {message}"

    except sqlite3.Error as e:
        return f"Database connection error: {e}"
