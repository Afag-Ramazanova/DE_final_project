from locust import HttpUser, task, between, events
import csv


class AnalyzeApiTest(HttpUser):
    wait_time = between(0.1, 0.5)  # Wait time between requests

    @task
    def analyze_endpoint(self):
        """Task to load test the /analyze endpoint."""
        response = self.client.get("https://zztaz2qbqh.us-east-2.awsapprunner.com")
        if response.status_code != 200:
            events.request.fire(
                request_type="GET",
                name="/analyze",
                response_time=response.elapsed.total_seconds(),
                response_length=len(response.content),
                exception=Exception(f"HTTP {response.status_code}: {response.text}"),
            )

    @events.test_start.add_listener
    def on_test_start(environment, **kwargs):
        """Set up CSV logging when the test starts."""
        with open("locust_results.csv", "w") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    "Request Type",
                    "Endpoint",
                    "Response Time (ms)",
                    "Response Length",
                    "Exception",
                ]
            )

    @events.request.add_listener
    def log_request(
        request_type, name, response_time, response_length, exception, **kwargs
    ):
        """Log all requests (success and failure) to a CSV."""
        with open("locust_results.csv", "a") as file:
            writer = csv.writer(file)
            writer.writerow(
                [request_type, name, response_time, response_length, str(exception)]
            )
