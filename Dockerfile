# Step 1: Use a Python builder image to install dependencies
FROM python:3.9-slim as builder

# Set the working directory in the builder image
WORKDIR /app

# Copy the application code and requirements
COPY . /app

# Install dependencies in a separate directory to avoid polluting the system
RUN pip install --no-cache-dir --target=/app/dependencies -r requirements.txt

# Step 2: Use a distroless base image
FROM gcr.io/distroless/python3-debian12

# Set the working directory in the final image
WORKDIR /app

# Copy only the application code and dependencies from the builder
COPY --from=builder /app /app

# Set the environment variable for Flask
ENV FLASK_APP=main.py

# Expose the required port
EXPOSE 5000

# Command to run the application using Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]


# # Use the official Python image from the Docker Hub
# FROM python:3.9-slim

# # Set the working directory in the container
# # this allows for any subsequent commands to be run from this directory
# WORKDIR /app

# # Copy the current directory contents into the container at /app
# # . indicates the directory where the Dockerfile is located and copies all 
# # files in that directory into our container working directory
# COPY . /app

# # Install any needed packages specified in requirements.txt
# # using --no-cache-dir to not cache the packages and save space
# RUN pip install --no-cache-dir -r requirements.txt

# # Make port 5000 available to the world outside this container
# EXPOSE 5000

# # Define environment variable
# # FLASK_APP is a framework specific environmnent variable that tells
# # the flask command where the application is located

# #without this the flask run command will not know what app to run.
# ENV FLASK_APP=main.py

# # Run app.py when the container launches
# # 0.0.0.0 sets the application to listen on all network interfaces

# #a more secure option would be to specify the exact IP you plan to use 
# # (e.g.API gateway interface)
# CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
# #CMD ["flask", "run", "--host=0.0.0.0"]