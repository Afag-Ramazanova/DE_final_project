import sqlite3
import boto3
import json
from botocore.exceptions import ClientError

# Path to your SQLite database
db_path = "/Users/tusunaiturumbekova/DE_final_project/data/products.db"

# Create a Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-west-2")


def convert_to_sql(user_prompt):
    # Updated prompt with schema details
    prompt = (
        "The database has the following schema: "
        "products(name, main_category, sub_category, ratings, no_of_ratings, discount_price, actual_price). "
        "All string columns (name, main_category, sub_category) need to be UPPERCASEd. "
        "If calculating the standard deviation, use the formula to approximate it. "
        f"Convert the following natural language query into a SQL query: {user_prompt}"
    )

    # Format the request payload for the LLM
    native_request = {
        "modelId": "anthropic.claude-3-5-haiku-20241022-v1:0",
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps(
            {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 200,
                "top_k": 250,
                "temperature": 0,
                "top_p": 0.999,
                "messages": [{"role": "user", "content": prompt}],
            }
        ),
    }

    try:
        response = client.invoke_model(**native_request)
        model_response = json.loads(response["body"].read())

        # Log full model response for debugging
        print("Full Model Response:", model_response)

        # Extract SQL query from nested structure
        raw_content_list = model_response.get("content", [])
        raw_content = raw_content_list[0].get("text", "") if raw_content_list else ""

        # Extract SQL from response content
        if "```sql" in raw_content:
            start_idx = raw_content.find("```sql") + len("```sql")
            end_idx = raw_content.find("```", start_idx)
            sql_query = raw_content[start_idx:end_idx].strip()

            # Normalize query strings to ensure case insensitivity
            sql_query = sql_query.replace("sub_category =", "UPPER(sub_category) =")
        else:
            sql_query = raw_content.strip()

        # Fallback for empty query
        if not sql_query:
            print(
                "The model did not generate a valid SQL query. Falling back to a predefined query."
            )

        print("Extracted SQL Query:", sql_query)
        return sql_query
    except ClientError as e:
        raise Exception(f"Bedrock ClientError: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")


def execute_sql_query(sql_query):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        conn.close()
        return result
    except sqlite3.OperationalError as e:
        raise Exception(f"SQLite Operational Error: {e}")
    except sqlite3.DatabaseError as e:
        raise Exception(f"SQLite Database Error: {e}")
    except Exception as e:
        raise Exception(f"Unexpected Error: {e}")


def generate_combined_response(user_prompt, query_result):
    try:
        # Analyze query results
        if not query_result:
            result_text = (
                "No results were found. Please check your query or the database."
            )
        elif len(query_result[0]) == 1:  # Single-column result
            result_value = query_result[0][0]
            # Handle single-value results
            if len(query_result) == 1:
                if isinstance(result_value, (int, float)):  # Single numeric result
                    result_text = f"{result_value:,.2f}"  # Format as float
                elif isinstance(result_value, str):  # Single text result
                    result_text = result_value
                else:
                    result_text = str(result_value)  # Fallback for other types
            else:  # Multiple single-column rows
                result_count = len(query_result)
                if result_count > 50:  # Summarize if too many results
                    examples = ", ".join(str(row[0]) for row in query_result[:5])
                    result_text = (
                        f"The query returned {result_count} results. "
                        f"Examples include: {examples}, and many more."
                    )
                else:  # Display all results
                    result_text = ", ".join(str(row[0]) for row in query_result)
        else:  # Multi-column result
            result_count = len(query_result)
            if result_count > 10:  # Summarize for large multi-column datasets
                example_rows = "; ".join(
                    ", ".join(map(str, row)) for row in query_result[:3]
                )
                result_text = (
                    f"The query returned {result_count} rows with multiple fields. "
                    f"Examples include: {example_rows}, and more."
                )
            else:  # Display all rows
                result_text = "; ".join(
                    ", ".join(map(str, row)) for row in query_result
                )

        # Generalize LLM prompt
        prompt = (
            f"The user asked: '{user_prompt}'. "
            f"The result of their query is: {result_text}. "
            "Please provide a natural language response to convey this information."
        )

        # Log for debugging
        print(f"LLM Prompt: {prompt}")

        # Prepare the request payload for the LLM
        native_request = {
            "modelId": "anthropic.claude-3-5-haiku-20241022-v1:0",
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": 300,
                    "top_k": 250,
                    "temperature": 1,
                    "top_p": 0.999,
                    "messages": [{"role": "user", "content": prompt}],
                }
            ),
        }

        # Call the LLM
        response = client.invoke_model(**native_request)
        model_response = json.loads(response["body"].read())

        # Log the full response for debugging
        print(f"Full Model Response: {model_response}")

        # Extract natural language response
        raw_content_list = model_response.get("content", [])
        raw_content = raw_content_list[0].get("text", "") if raw_content_list else ""

        print(f"Raw LLM Response: {raw_content}")  # Debugging

        if raw_content:
            return raw_content.strip()
        else:
            return f"The result of your query is: {result_text}."

    except ClientError as e:
        return f"Error: Bedrock ClientError: {e}"
    except Exception as e:
        return f"Error: {e}"


def validate_sql_query(sql_query):
    if "SELECT" not in sql_query or "FROM" not in sql_query:
        return False
    return True


def main():
    user_prompt = (
        "What are the top 3 most expensive items in the 'Car Electronics' sub-category?"
    )
    try:
        user_prompt = user_prompt.upper()  # Ensure case consistency
        sql_query = convert_to_sql(user_prompt)
        if not sql_query.strip():
            print("Generated SQL Query is empty or invalid.")
            return

        print("Generated SQL Query:", sql_query)

        query_result = execute_sql_query(sql_query)
        print("Query Result:", query_result)

        if not query_result:
            print("No results found.")
            return

        combined_response = generate_combined_response(user_prompt, query_result)
        print("Response:", combined_response)

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
