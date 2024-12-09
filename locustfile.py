from locust import HttpUser, task, between
import random

class TextToSQLUser(HttpUser):
    wait_time = between(1, 5)  # Simulates a user waiting time between requests
    
    @task
    def ask_inventory_question(self):
        # Sample questions to randomly choose from
        questions = [
        "What is the average actual price of items in the 'Car Electronics' sub-category?",
        "How many items in the 'Car Electronics' sub-category have a rating greater than 4.0?",
        "What are the top 3 most expensive items in the 'Car Electronics' sub-category?",
        ]
        # Randomly pick a question
        question = random.choice(questions)
        
        # Payload for the API
        payload = {"query": question}
        
        # Send POST request to the text-to-SQL endpoint
        self.client.post("https://zztaz2qbqh.us-east-2.awsapprunner.com", json=payload)

    # Add other @task methods for more endpoint tests if required
