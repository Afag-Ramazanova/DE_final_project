import logging
from flask import Flask, render_template, request
import csv
from datetime import datetime
from lib.llm import convert_to_sql, execute_sql_query, generate_combined_response

app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",  # Log format
    handlers=[
        logging.StreamHandler(),  # Output to stdout (Gunicorn will capture this)
        logging.FileHandler("app.log")  # Log to a file
    ]
)

logger = logging.getLogger()

@app.route("/")
def index():
    logger.info("Index page accessed")
    return render_template("webpage.html")

@app.route("/schema")
def schema():
    logger.info("Schema page accessed")
    return render_template("schema.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    # Get the message from the form
    message = request.form["chatMessage"]
    logger.info(f"Received message: {message}")

    # Log the message with the timestamp in message.csv
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("message.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([message, timestamp])
    logger.info(f"Logged message at {timestamp}")

    try:
        # Step 1: Convert the message to an SQL query using LLM
        sql_query = convert_to_sql(message)
        logger.debug(f"Generated SQL query: {sql_query}")

        # Handle invalid or empty SQL query
        if not sql_query.strip():
            logger.warning(f"Invalid SQL query for message: {message}")
            return render_template(
                "webpage.html",
                message=message,
                sql_query="Invalid SQL query",
                query_result="No results",
                natural_language_result="Sorry, no query could be generated.",
            )

        # Step 2: Execute the SQL query to retrieve the results from the database
        query_result = execute_sql_query(sql_query)
        logger.debug(f"Query results: {query_result}")

        # Handle if no query results were found
        if not query_result:
            logger.warning(f"No results found for SQL query: {sql_query}")
            return render_template(
                "webpage.html",
                message=message,
                sql_query=sql_query,
                query_result="No results found",
                natural_language_result="Sorry, no results were found.",
            )

        # Step 3: Generate a natural language response from the query results
        natural_language_result = generate_combined_response(message, query_result)
        logger.debug(f"Natural language result: {natural_language_result}")

        # Pass the results to the template for rendering
        return render_template(
            "webpage.html",
            message=message,
            sql_query=sql_query,
            query_result=query_result,
            natural_language_result=natural_language_result,
        )

    except Exception as e:
        logger.error(f"Error occurred: {e}")
        # In case of an error, render an error message
        return render_template(
            "webpage.html",
            message=message,
            sql_query="Error",
            query_result="Error",
            natural_language_result=f"Error: {e}",
        )


if __name__ == "__main__":
    app.run(debug=True)
