from flask import Flask, render_template, request
import csv
from datetime import datetime
import data  # Import functions from data.py

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('webpage.html')  # Render the HTML template

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the message from the form
    message = request.form['chatMessage']
    
    # Log the message with the timestamp in message.csv
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('message.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([message, timestamp])
    
    # Pass the message to data.py and get the result
    result = data.process_message(message)  # Capture the result from process_message
    
    # Return the result to the user (or send it to a different template for rendering)
    return f"Message received: {message} <br> Query Result: {result}"

if __name__ == '__main__':
    app.run(debug=True)
