import pytest
import pymysql
from lib.llm import convert_to_sql, generate_combined_response
from dotenv import load_dotenv
import os

# # Load environment variables from .env file
# load_dotenv()

# # Setup the database connection parameters from environment variables

# db_host = os.getenv("RDS_HOST")
# db_user = os.getenv("RDS_USER")
# db_password = os.getenv("RDS_PASSWORD")
# db_name = os.getenv("RDS_NAME")



# # Make sure the required environment variables are loaded
# assert db_host, "RDS_HOST is not set"
# assert db_user, "RDS_USER is not set"
# assert db_password, "RDS_PASSWORD is not set"
# assert db_name, "RDS_NAME is not set"


import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Fetch database credentials
db_host = os.getenv("RDS_HOST")
db_user = os.getenv("RDS_USER")
db_password = os.getenv("RDS_PASSWORD")
db_name = os.getenv("RDS_NAME")

# Log loaded environment variables (without sensitive data)
logging.info(f"Loaded DB Host: {db_host}")
logging.info(f"Using DB User: {db_user}")

# Validate credentials
if not all([db_host, db_user, db_password, db_name]):
    raise EnvironmentError("One or more required environment variables are missing.")


# Setup the database connection using AWS RDS (No SQLite setup needed)
def execute_sql_query(sql_query):
    try:
        # Connect to the AWS RDS database using pymysql
        connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name,
        )

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        return result

    except pymysql.MySQLError as e:
        raise Exception(f"MySQL Error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected Error: {e}")
    finally:
        # Ensure the connection is always closed
        connection.close()


# prompts for testing
prompts = [
    "What is the average actual price of items in the 'Car Electronics' sub-category?",
    "How many items in the 'Car Electronics' sub-category have a rating greater than 4.0?",
    "What are the top 3 most expensive items in the 'Car Electronics' sub-category?",
    "What is the average discount price for each sub-category within the 'Car & Motorbike' main category?",
    "What is the total discount price for items in the 'Nonexistent' sub-category?",
    "Find all items where the name contains the word 'Bluetooth'.",
    "Show me the names and discount prices of items in the 'Car Electronics' sub-category.",
]

# Test function to check the SQL query execution
@pytest.mark.parametrize("prompt", prompts)
def test_llm_with_db(prompt):
    # Generate SQL query from the LLM
    sql_query = convert_to_sql(prompt)

    # Check if the query is valid and add alias to subqueries if missing
    if "FROM (" in sql_query and "AS" not in sql_query.split("FROM")[-1]:
        # Fix: Add alias directly after the closing parenthesis of the subquery
        sql_query = sql_query.rstrip(")") + " AS subquery)"

    # Assert that the generated SQL query is not empty
    assert sql_query != "", f"Generated SQL query for prompt '{prompt}' is empty."
    print(f"Generated SQL query: {sql_query}")  # Debugging line

    # Execute the SQL query against the AWS RDS database
    query_result = execute_sql_query(sql_query)

    # Ensure the query result is not None or empty
    assert query_result is not None, f"Query result for prompt '{prompt}' is None."
    assert len(query_result) > 0, f"Query result for prompt '{prompt}' is empty."

    # Generate a natural language response based on the query result
    natural_language_result = generate_combined_response(prompt, query_result)

    # Ensure that the response does not contain "Error" or is not empty
    assert (
        "Error" not in natural_language_result
    ), f"Error found in response for prompt: {prompt}"
    assert natural_language_result != "", f"Empty response found for prompt: {prompt}"
