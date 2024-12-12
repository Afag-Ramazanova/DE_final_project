import sqlite3
import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError, PartialCredentialsError
import os
import pymysql
from dotenv import load_dotenv


load_dotenv()
# Create a Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-west-2")


def convert_to_sql(user_prompt):
    # Retrieve table name from environment
    table_name = os.getenv("table_name", "items")

    # List of main categories and sub-categories
    main_categories = [
        "ACCESSORIES",
        "APPLIANCES",
        "BAGS & LUGGAGE",
        "BEAUTY & HEALTH",
        "CAR & MOTORBIKE",
        "GROCERY & GOURMET FOODS",
        "HOME & KITCHEN",
        "HOME",
        "KITCHEN",
        "PETS",
        "INDUSTRIAL SUPPLIES",
        "KIDS' FASHION",
        "MEN'S CLOTHING",
        "MEN'S SHOES",
        "MUSIC",
        "PET SUPPLIES",
        "SPORTS & FITNESS",
        "STORES",
        "TOYS & BABY PRODUCTS",
        "TV, AUDIO & CAMERAS",
        "WOMEN'S CLOTHING",
        "WOMEN'S SHOES",
    ]
    sub_categories = [
        "AIR CONDITIONERS",
        "ALL APPLIANCES",
        "ALL CAR & MOTORBIKE PRODUCTS",
        "ALL ELECTRONICS",
        "ALL EXERCISE & FITNESS",
        "ALL GROCERY & GOURMET FOODS",
        "ALL HOME & KITCHEN",
        "ALL PET SUPPLIES",
        "ALL SPORTS, FITNESS & OUTDOORS",
        "AMAZON FASHION",
        "BABY BATH, SKIN & GROOMING",
        "BABY FASHION",
        "BABY PRODUCTS",
        "BACKPACKS",
        "BADMINTON",
        "BAGS & LUGGAGE",
        "BALLERINAS",
        "BEAUTY & GROOMING",
        "BEDROOM LINEN",
        "CAMERA ACCESSORIES",
        "CAMERAS",
        "CAMPING & HIKING",
        "CAR & BIKE CARE",
        "CAR ACCESSORIES",
        "CAR ELECTRONICS",
        "CAR PARTS",
        "CARDIO EQUIPMENT",
        "CASUAL SHOES",
        "CLOTHING",
        "COFFEE, TEA & BEVERAGES",
        "CRICKET",
        "CYCLING",
        "DIAPERS",
        "DIET & NUTRITION",
        "DOG SUPPLIES",
        "ETHNIC WEAR",
        "FASHION & SILVER JEWELLERY",
        "FASHION SALES & DEALS",
        "FASHION SANDALS",
        "FITNESS ACCESSORIES",
        "FOOTBALL",
        "FORMAL SHOES",
        "FURNITURE",
        "GARDEN & OUTDOORS",
        "GOLD & DIAMOND JEWELLERY",
        "HANDBAGS & CLUTCHES",
        "HEADPHONES",
        "HEALTH & PERSONAL CARE",
        "HEATING & COOLING APPLIANCES",
        "HOME AUDIO & THEATER",
        "HOME DÉCOR",
        "HOME ENTERTAINMENT SYSTEMS",
        "HOME FURNISHING",
        "HOME IMPROVEMENT",
        "HOME STORAGE",
        "HOUSEHOLD SUPPLIES",
        "INDOOR LIGHTING",
        "INDUSTRIAL & SCIENTIFIC SUPPLIES",
        "INNERWEAR",
        "INTERNATIONAL TOY STORE",
        "JANITORIAL & SANITATION SUPPLIES",
        "JEANS",
        "JEWELLERY",
        "KIDS' CLOTHING",
        "KIDS' FASHION",
        "KIDS' SHOES",
        "KIDS' WATCHES",
        "KITCHEN & DINING",
        "KITCHEN & HOME APPLIANCES",
        "KITCHEN STORAGE & CONTAINERS",
        "LAB & SCIENTIFIC",
        "LINGERIE & NIGHTWEAR",
        "LUXURY BEAUTY",
        "MAKE-UP",
        "MEN'S FASHION",
        "MOTORBIKE ACCESSORIES & PARTS",
        "MUSICAL INSTRUMENTS & PROFESSIONAL AUDIO",
        "NURSING & FEEDING",
        "PERSONAL CARE APPLIANCES",
        "REFRIGERATORS",
        "REFURBISHED & OPEN BOX",
        "RUCKSACKS",
        "RUNNING",
        "SCHOOL BAGS",
        "SECURITY CAMERAS",
        "SEWING & CRAFT SUPPLIES",
        "SHIRTS",
        "SHOES",
        "SNACK FOODS",
        "SPEAKERS",
        "SPORTS SHOES",
        "SPORTSWEAR",
        "STEM TOYS STORE",
        "STRENGTH TRAINING",
        "STROLLERS & PRAMS",
        "SUITCASES & TROLLEY BAGS",
        "SUNGLASSES",
        "T-SHIRTS & POLOS",
        "TELEVISIONS",
        "TEST, MEASURE & INSPECT",
        "THE DESIGNER BOUTIQUE",
        "TOYS & GAMES",
        "TOYS GIFTING STORE",
        "TRAVEL ACCESSORIES",
        "TRAVEL DUFFLES",
        "VALUE BAZAAR",
        "WALLETS",
        "WASHING MACHINES",
        "WATCHES",
        "WESTERN WEAR",
        "WOMEN'S FASHION",
        "YOGA",
    ]

    # Normalize user prompt by replacing 'and' with '&' where applicable
    normalized_prompt = user_prompt.upper().replace(" AND ", " & ")

    # Build the prompt dynamically based on schema
    prompt = (
        f"The database has the following schema: "
        f"{table_name}(name, main_category, sub_category, ratings, no_of_ratings, "
        f"discount_price, actual_price). "
        "All string columns (name, main_category, sub_category) need to be UPPERCASEd. "
        f"If the prompt involves categories from {main_categories}, use 'main_category'. "
        f"If it involves categories from {sub_categories}, use 'sub_category'. "
        f"Convert the following natural language query into a MySQL query: {normalized_prompt}."
    )

    # Prepare the request payload for the LLM
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

        # Extract SQL query from the LLM response
        raw_content_list = model_response.get("content", [])
        raw_content = raw_content_list[0].get("text", "") if raw_content_list else ""

        # Extract SQL from response content if markdown exists
        if "```sql" in raw_content:
            start_idx = raw_content.find("```sql") + len("```sql")
            end_idx = raw_content.find("```", start_idx)
            sql_query = raw_content[start_idx:end_idx].strip()
            sql_query = sql_query.replace("sub_category =", "UPPER(sub_category) =")
            sql_query = sql_query.replace("main_category =", "UPPER(main_category) =")
        else:
            sql_query = raw_content.strip()

        if not validate_sql_query(sql_query):
            return "This query does not match any valid database schema. Please try a different query."

        print("Extracted SQL Query:", sql_query)
        return sql_query

    except ClientError as e:
        raise Exception(f"Bedrock ClientError: {e}")
    except NoCredentialsError:
        raise Exception(f"Bedrock NoCredentialsError: {e}")
        # print("No credentials found. Ensure environment variables or IAM role are set correctly.")
    except PartialCredentialsError as e:
        raise Exception(f"Bedrock PartialCredentialsError: {e}")
        # print(f"Partial credentials error: {e}")
    except Exception as e:
        raise Exception(f"Error: {e}")


def execute_sql_query(sql_query):
    try:
        # Connect to the AWS RDS database
        connection = pymysql.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME"),
        )

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            result = cursor.fetchall()

        connection.close()
        return result

    except pymysql.MySQLError as e:
        raise Exception(f"MySQL Error: {e}")
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
    user_prompt = "most expensive item in women's clothing"
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
