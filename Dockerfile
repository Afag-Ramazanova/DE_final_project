# Use an official Python image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy your project files into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port Flask/Gunicorn will run on
EXPOSE 8000

# Use Gunicorn to serve your Flask app
CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "--workers", "4"]