from flask import Flask, render_template, request
import csv
from datetime import datetime
import data  # Import functions from data.py
from lib.llm import convert_to_sql, execute_sql_query, generate_combined_response  # Correctly import the functions from llm.py

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("webpage.html")  # Render the HTML template

@app.route("/analyze", methods=["POST"])
def analyze():
    # Get the message from the form
    message = request.form["chatMessage"]

    # Log the message with the timestamp in message.csv
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("message.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([message, timestamp])

    try:
        # Step 1: Convert the message to an SQL query using LLM
        sql_query = convert_to_sql(message)
        
        # Handle invalid or empty SQL query
        if not sql_query.strip():
            return render_template(
                "webpage.html", 
                message=message, 
                sql_query="Invalid SQL query", 
                query_result="No results", 
                natural_language_result="Sorry, no query could be generated."
            )

        # Step 2: Execute the SQL query to retrieve the results from the database
        query_result = execute_sql_query(sql_query)

        # Handle if no query results were found
        if not query_result:
            return render_template(
                "webpage.html", 
                message=message, 
                sql_query=sql_query, 
                query_result="No results found", 
                natural_language_result="Sorry, no results were found."
            )

        # Step 3: Generate a natural language response from the query results
        natural_language_result = generate_combined_response(message, query_result)

        # Pass the results to the template for rendering
        return render_template(
            "webpage.html",
            message=message,
            sql_query=sql_query,
            query_result=query_result,
            natural_language_result=natural_language_result,
        )

    except Exception as e:
        # In case of an error, render an error message
        return render_template("webpage.html", message=message, sql_query="Error", query_result="Error", natural_language_result=f"Error: {e}")

if __name__ == "__main__":
    app.run(debug=True)
