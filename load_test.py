from locust import HttpUser, TaskSet, task, between


class UserBehavior(TaskSet):
    @task(1)
    def load_test_endpoint(self):
        self.client.get("https://zztaz2qbqh.us-east-2.awsapprunner.com/")  # Replace with your API endpoint
        # Or for a POST request:
        # self.client.post("/your-endpoint", json={"key": "value"})


class LoadTestUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(1, 3)  # Wait between 1 to 3 seconds between tasks
