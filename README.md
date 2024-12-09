Check CI/CD Status: 

[![Install Dependencies](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/install.yml/badge.svg)](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/install.yml) [![Lint Code](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/lint.yml/badge.svg)](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/lint.yml) [![Format Code](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/format.yml/badge.svg)](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/format.yml) [![Test Code](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/test.yml/badge.svg)](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/test.yml) [![Deploy App to AWS AppRunner](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/ecr.yml/badge.svg)](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/ecr.yml) [![Deploy RDS with CloudFormation](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/deploy_rds.yml/badge.svg)](https://github.com/Afag-Ramazanova/DE_final_project/actions/workflows/deploy_rds.yml)
# AskSQl Natural Language to SQL Microservice
<img src="static/images/logo_new.png" alt="logo" width="400" height="150"> 

#### Contributors:
[Afag Ramazanova](https://github.com/Afag-Ramazanova),
[Loo Si Min (Lucy)](https://github.com/loosimin16),
[Rishika Randev](https://github.com/rrandev03),
[Seijung Kim](https://github.com/seij001),
[Tursunai Turumbekova](https://github.com/tursunait)

## Overview
This project is a **microservice solution** designed to empower businesses to interact with their Invenroty database on AWS RDS using **natural language questions**, removing the need for SQL expertise. It is a robust and scalable application that leverages AWS services and cutting-edge AI to convert human-readable queries into SQL commands, retrieve data from the database, and respond with answers in natural language. It leverages AWS services and AI-powered tools to deliver an efficient, cloud-native experience.

### Key Features:
- **Microservice Architecture**: Built as a standalone, containerized microservice using a Docker image.
- **User-friendly Interface**: A simple web application for inputting natural language questions.
- **AI-Powered SQL Conversion**: Utilizes **Anthropic Claude 3.5** through AWS Bedrock to convert questions into SQL queries.
- **Database Interaction**: Queries data from an **AWS RDS** database.
- **Natural Language Responses**: Returns the results in natural language, displayed on the web page.
- **Cloud-Native Deployment**: Hosted on AWS using **AppRunner**, with container images stored in **ECR**.
- **Performance Validated**: Load-tested to handle 10,000 requests per second.
- **CI/CD Integration**: Automated pipeline for dependency installation, code linting, formatting, testing, and deployment.
- **Infrastructure as Code**: Fully deployed using AWS CloudFormation for infrastructure setup and management.


## Use Case
This microservice is designed for **business (inventory) users** who need actionable insights from their databases but lack SQL expertise. For this implementation, the database is an **Amazon inventory database**, containing the following columns:
- `name`
- `main_category`
- `sub_category`
- `ratings`
- `no_of_ratings`
- `discount_price`
- `actual_price`

This application is ideal for: retail inventory analysis, sales trend exploration, product category performance evaluation, etc. 

### Example Queries:
- "Can you find all items with Bluetooth in their name?"
- "Could you show me the names and discount prices of all items in the Car Electronics sub-category"
- "How many products have a rating higher than 4.5?"

## Architecture
The application architecture is built entirely on AWS, ensuring scalability, reliability, and performance:
1. **Web Interface**: Built with Flask for user interaction.
2. **Query Conversion**: Natural language questions are sent to **Anthropic Claude 3.5** via AWS Bedrock to generate SQL queries.
3. **Database Interaction**: SQL queries are executed against an **AWS RDS** database.
4. **Response Handling**: Results are translated back into natural language and displayed on the web interface.
5. **Deployment**: The application is containerized and deployed on **AWS AppRunner**, pulling images from **AWS ECR**.

![Architecture](static/images/IDS706_Final_Architecture.png)

## Technology Stack
- **Backend**: Flask (Python)
- **Programming Language**: Python
- **Framework**: Flask
- **AI Model**: Anthropic Claude 3.5 (via AWS Bedrock)
- **Database**: AWS RDS (Relational Database Service)
- **Cloud Services**:
  - AWS AppRunner
  - AWS Elastic Container Registry (ECR)
  - AWS Bedrock
  - AWS CloudFormation (IaC)
- **Load Testing**: Validated with a tool to ensure 10,000 requests per second.

- **CI/CD Pipeline**:
  - Install dependencies
  - Lint and format code
  - Test application
  - Build and push container image to ECR
  - Deploy to AWS AppRunner

## Deployment Instructions
1. **Prerequisites**:
   - AWS account with access to AppRunner, ECR, RDS, and Bedrock.
   - Docker installed locally.
   - AWS CLI configured.
2. **Clone Repository**:
   ```bash
   git clone <repository_url>
   cd <project_directory>
   ```
3. **Build and Push Docker Image**:
   ```bash
   docker build -t <image_name> .
   docker tag <image_name> <ecr_repository_url>
   docker push <ecr_repository_url>
   ```
4. **Deploy to AppRunner**:
   Use the AWS Management Console or CLI to create an AppRunner service pulling the container image from ECR.

## CI/CD Pipeline
The project includes a CI/CD pipeline for streamlined development and deployment. The pipeline consists of the following stages:
1. **Install Dependencies**: Ensures all required packages are installed.
2. **Lint Code**: Checks for code quality and adherence to standards.
3. **Format Code**: Automatically formats code for consistency.
4. **Test Code**: Runs automated tests to validate functionality.
5. **Deploy**: Builds and pushes the Docker image to ECR. AppRunner service is set up to automatically re-deploy the app when a new container image is pushed to ECR repository.

## Quantitative Assessment

The system has been load-tested to handle 10,000 requests per second. Key metrics include:
- **Average Latency**: Measured across various request loads (100, 1,000, 10,000).
- **Error Rates**: Maintained under acceptable thresholds during testing.

- The detailed assessment is accessible here: [PDF](quant_assessment/Locustfinal.pdf), [CSV](quant_assessment/Locust_2024-12-09-13h05_load_test.py_https___zztaz2qbqh.us-east-2.awsapprunner.com_requests.csv)

![request](quant_assessment/request_stats.png)

## Demo Video

A video walkthrough demonstrating the application, including load testing and performance metrics, can be found here.

## How It Works
1. The user inputs a natural language question via the web interface.
2. The app sends the question to **Anthropic Claude 3.5** through AWS Bedrock.
3. The AI generates an SQL query tailored to the question.
4. The SQL query is executed on the **AWS RDS** database.
5. The results are converted back to natural language and displayed to the user.

## Future Enhancements
- Support for additional databases.
- Enhanced natural language understanding for complex queries.
- Advanced visualization options for query results.


Thank you!
