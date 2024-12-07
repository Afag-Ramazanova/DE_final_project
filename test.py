import pytest
import sqlite3
from lib.llm import convert_to_sql, execute_sql_query, generate_combined_response

db_path = "data/products.db"

# Setup the database by connecting to SQLite file
def setup_test_db():
    conn = sqlite3.connect(db_path)
    return conn

def teardown_test_db(conn):
    conn.close()  # Cleanup the database connection after each test

# Define the prompts for testing
prompts = [
    ("What is the average actual price of items in the 'Car Electronics' sub-category?"),
    ("How many items in the 'Car Electronics' sub-category have a rating greater than 4.0?"),
    ("What are the top 3 most expensive items in the 'Car Electronics' sub-category?"),
    ("What is the average discount price for each sub-category within the 'Car & Motorbike' main category?"),
    ("What is the total discount price for items in the 'Nonexistent' sub-category?"),
    ("Find all items where the name contains the word 'Bluetooth'."),
    ("What is the standard deviation of the discount price for items in the 'Car Electronics' sub-category?"),
    ("Show me the names and discount prices of items in the 'Car Electronics' sub-category.")
]

@pytest.mark.parametrize("prompt", prompts)
def test_llm_with_db(prompt):
    # Setup test database connection
    conn = setup_test_db()
    
    # Mock the LLM response generation function (for SQL query conversion and final response)
    sql_query = convert_to_sql(prompt)
    
    # Assert that the generated SQL query is not empty (it should return something valid)
    assert sql_query != "", f"Generated SQL query for prompt '{prompt}' is empty."
    
    query_result = execute_sql_query(sql_query)
    
    # Ensure the query result is not None or empty
    assert query_result is not None, f"Query result for prompt '{prompt}' is None."
    assert len(query_result) > 0, f"Query result for prompt '{prompt}' is empty."
    
    natural_language_result = generate_combined_response(prompt, query_result)
    
    # Ensure that the response does not contain "Error" or is not empty
    assert "Error" not in natural_language_result, f"Error found in response for prompt: {prompt}"
    assert natural_language_result != "", f"Empty response found for prompt: {prompt}"
    
    # Teardown the test database after the test
    teardown_test_db(conn)