# // [TASK]: Create Locust load test scenario
# // [GOAL]: Simulate user traffic to the application
# // [ELITE_CURSOR_SNIPPET]: aihandle

from locust import HttpUser, task, between

class WebsiteUser(HttpUser):
    wait_time = between(1, 2.5)

    @task
    def health_check(self):
        self.client.get("/health")

    @task(3)
    def register_user(self):
        self.client.post("/register", json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
            "tenant_name": "testtenant"
        })