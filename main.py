from flask import Flask, render_template, request
import csv
from datetime import datetime
import data  # Import functions from data.py
from lib.llm import generate_response  ##getting the response from the LLM

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


    # Step 1: Pass the message to LLM to convert it into an SQL query
    llm_prompt = f"Convert the following message to SQL: {message}"  # pass to llm
    sql_query = generate_response(llm_prompt)  # get the llm response as a query

    # Step 2: Use the SQL query in the database
    query_result = data.process_message(sql_query)

    # Step 3: Pass the query result to the LLM for conversion to normal text
    llm_prompt_result = f"Convert this SQL query result into a user-friendly description: {query_result}"
    natural_language_result = generate_response(llm_prompt_result)

    # Pass the results to the template for rendering
    return render_template(
        "webpage.html",
        message=message,
        sql_query=sql_query,
        query_result=query_result,
        natural_language_result=natural_language_result,
    )

    # Pass the message to data.py and get the result
    # result = data.process_message(message)  # Capture the result from process_message

    # Return the result to the user (or send it to a different template for rendering)
    # return f"Message received: {message} <br> Query Result: {result}"


if __name__ == "__main__":
    app.run(debug=True)