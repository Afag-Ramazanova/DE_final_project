# Define the image name
IMAGE_NAME = mini_12_rr
DOCKER_ID_USER = rrandev25

# Install dependencies
install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

# Run tests in the backend folder
test:
	python -m pytest -vv backend/test_*.py

# Format Python code
format:
	black .

# Lint Python code
lint:
	ruff check backend/*.py

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
run:
	docker run -p 5000:5000 $(IMAGE_NAME)

# Remove the Docker image
clean:
	docker rmi $(IMAGE_NAME)

# Show Docker images
image_show:
	docker images

# Show running Docker containers
container_show:
	docker ps

# Push the Docker image to Docker Hub
push:
	docker login
	docker tag $(IMAGE_NAME) $(DOCKER_ID_USER)/$(IMAGE_NAME)
	docker push $(DOCKER_ID_USER)/$(IMAGE_NAME):latest

# Login to Docker
login:
	docker login -u ${DOCKER_ID_USER}

# Default target: Run all tasks
all: install lint test format build push
