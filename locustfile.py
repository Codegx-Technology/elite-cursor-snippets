from locust import HttpUser, task, between
import json
import os
import random

class ShujaaStudioUser(HttpUser):
    wait_time = between(1, 5) # Simulate user thinking time between tasks
    host = "http://localhost:8000" # Assuming FastAPI server runs on this host/port

    # User credentials for login
    # In a real scenario, these would be loaded securely (e.g., from environment variables)
    # or generated dynamically for test users.
    TEST_USERNAME = os.getenv("LOCUST_TEST_USERNAME", "testuser")
    TEST_PASSWORD = os.getenv("LOCUST_TEST_PASSWORD", "testpassword")

    def on_start(self):
        """On start of a Locust user, log in and get a JWT token."""
        self.client.headers = {} # Clear headers from previous runs
        self.login()

    def login(self):
        """Logs in the user and stores the access token."""
        response = self.client.post(
            "/token",
            data={"username": self.TEST_USERNAME, "password": self.TEST_PASSWORD},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        if response.status_code == 200:
            token = response.json()["access_token"]
            self.client.headers = {"Authorization": f"Bearer {token}"}
            self.environment.runner.stats.log_request(
                "POST", "/token", response.elapsed.total_seconds(), response.status_code
            )
            print(f"User {self.TEST_USERNAME} logged in successfully.")
        else:
            print(f"Login failed for user {self.TEST_USERNAME}: {response.status_code} {response.text}")
            self.environment.runner.quit() # Stop the user if login fails

    @task(3) # Higher weight for single video generation
    def generate_single_video(self):
        """Simulates a single video generation request."""
        prompt = "A cinematic story about innovation in Kenya."
        payload = {
            "prompt": prompt,
            "upload_youtube": False
        }
        response = self.client.post(
            "/generate_video",
            json=payload,
            name="/generate_video [single]" # Custom name for stats
        )
        if response.status_code != 200:
            print(f"Single video generation failed: {response.status_code} {response.text}")

    @task(1) # Lower weight for batch video generation
    def generate_batch_video(self):
        """Simulates a batch video generation request."""
        batch_requests = []
        for i in range(random.randint(2, 5)): # Generate 2-5 videos in a batch
            prompt = f"A short story about Kenyan wildlife {i}."
            batch_requests.append({
                "prompt": prompt,
                "upload_youtube": False
            })
        
        payload = {
            "requests": batch_requests
        }
        response = self.client.post(
            "/batch_generate_video",
            json=payload,
            name="/batch_generate_video [batch]" # Custom name for stats
        )
        if response.status_code != 200:
            print(f"Batch video generation failed: {response.status_code} {response.text}")

    @task(0) # Very low weight, mostly for setup/monitoring
    def health_check(self):
        """Checks the health endpoint."""
        self.client.get("/health", name="/health")