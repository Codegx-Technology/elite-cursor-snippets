import os
from locust import HttpUser, task, between

# --- Test Configuration ---
# In a real scenario, this token would be fetched via a login flow or from a secure store.
# For this test, you need to manually get a token by running the api_server,
# hitting the /token endpoint with a registered user, and pasting the access_token here.
# You can also set it as an environment variable: export LOCUST_TEST_TOKEN="your-token"
JWT_TOKEN = os.getenv("LOCUST_TEST_TOKEN", "your-jwt-token-here") 
HEADERS = {"Authorization": f"Bearer {JWT_TOKEN}"}

class ShujaaStudioUser(HttpUser):
    """
    Simulates a user interacting with the Shujaa Studio API.
    """
    wait_time = between(2, 6)  # Wait 2-6 seconds between tasks

    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        if JWT_TOKEN == "your-jwt-token-here":
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
            print("!!! WARNING: Using default placeholder JWT token.           !!!")
            print("!!! Authenticated endpoints will fail with 401 Unauthorized.!!!")
            print("!!! Set the LOCUST_TEST_TOKEN environment variable.         !!!")
            print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")

    @task(1)
    def health_check(self):
        """Task to check the health of the API."""
        self.client.get("/health", name="/health")

    @task(5)
    def generate_single_video(self):
        """Task to simulate generating a single video."""
        payload = {
            "prompt": "A short story about a lion cub exploring the savanna, cinematic style"
        }
        self.client.post("/generate_video", json=payload, headers=HEADERS, name="/generate_video")

    @task(2)
    def generate_batch_video(self):
        """Task to simulate generating a batch of videos."""
        payload = {
            "requests": [
                {"prompt": "A developer in Nairobi fixing a critical bug at midnight, lo-fi music"},
                {"prompt": "A drone flying over the tea fields of Kericho, epic cinematic drone shot"},
                {"prompt": "A group of friends enjoying a safari in Maasai Mara, laughing and pointing at animals"}
            ]
        }
        self.client.post(
            "/batch_generate_video",
            json=payload,
            headers=HEADERS,
            name="/batch_generate_video"
        )

    @task(2)
    def get_user_profile(self):
        """Task to get the current user's profile."""
        self.client.get("/users/me", headers=HEADERS, name="/users/me")

# To run this test:
# 1. Make sure the FastAPI server is running: uvicorn api_server:app --reload
# 2. Get a valid JWT token and set it as an environment variable:
#    export LOCUST_TEST_TOKEN="<your_token>"
# 3. Run Locust:
#    locust -f load_test.py --host http://localhost:8000
# 4. Open your browser to http://localhost:8089 and start the test.
