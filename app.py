from flask import Flask, request, render_template

app = Flask(__name__)


# Route for the calculator form
@app.route("/")
def calculator():
    return render_template("calculator.html")


# Route to handle calculation
@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        # Get the form data
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        operation = request.form["operation"]

        # Perform the calculation based on the selected operation
        if operation == "add":
            result = num1 + num2
        elif operation == "subtract":
            result = num1 - num2
        elif operation == "multiply":
            result = num1 * num2
        elif operation == "divide":
            if num2 != 0:
                result = num1 / num2
            else:
                return "Error: Division by zero is not allowed."
        else:
            return "Error: Invalid operation."

        return f"The result is: {result}"
    except ValueError:
        return "Error: Please enter valid numbers."


if __name__ == "__main__":
    app.run(debug=True)
