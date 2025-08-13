import requests
import json
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin
from error_utils import retry_on_exception

class ShujaaSDK:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    @retry_on_exception()
    def _request(self, method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None, idempotency_key: Optional[str] = None) -> Dict:
        headers = self.headers.copy()
        if idempotency_key:
            headers["X-Idempotency-Key"] = idempotency_key
        url = urljoin(self.base_url, endpoint)
        try:
            response = requests.request(method, url, headers=headers, json=data, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            print(f"Timeout Error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            print(f"Request Error: {e}")
            raise

    def get_health(self) -> Dict:
        """Checks the health of the API."""
        return self._request("GET", "/health")

    def register_user(self, username: str, email: str, password: str, tenant_name: Optional[str] = "default") -> Dict:
        """Registers a new user."""
        data = {"username": username, "email": email, "password": password, "tenant_name": tenant_name}
        return self._request("POST", "/register", data=data)

    def get_token(self, username: str, password: str) -> Dict:
        """Gets an access token for a user."""
        # FastAPI's /token endpoint expects form data, not JSON
        data = {"username": username, "password": password}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            response = requests.post(urljoin(self.base_url, "/token"), headers=headers, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Token Request Error: {e}")
            raise

    def get_user_profile(self) -> Dict:
        """Retrieves the current user's profile."""
        return self._request("GET", "/users/me")

    def update_user_profile(self, email: Optional[str] = None, full_name: Optional[str] = None, bio: Optional[str] = None) -> Dict:
        """Updates the current user's profile."""
        data = {k: v for k, v in locals().items() if k != 'self' and v is not None}
        return self._request("PUT", "/users/me", data=data)

    def get_user_plan(self) -> Dict:
        """Retrieves the current user's plan details."""
        return self._request("GET", "/users/me/plan")

    def get_user_usage(self) -> Dict:
        """Retrieves the current user's usage statistics."""
        return self._request("GET", "/users/me/usage")

    def generate_video(self, prompt: str, news_url: Optional[str] = None, script_file: Optional[str] = None, upload_youtube: bool = False) -> Dict:
        """Generates a video based on a prompt, news URL, or script file."""
        data = {"prompt": prompt, "news_url": news_url, "script_file": script_file, "upload_youtube": upload_youtube}
        return self._request("POST", "/generate_video", data=data)

    def batch_generate_video(self, requests: List[Dict]) -> Dict:
        """Generates multiple videos in a batch."""
        data = {"requests": requests}
        return self._request("POST", "/batch_generate_video", data=data)

    def generate_landing_page(self, qr_code_id: str, brand_metadata: Dict) -> Dict:
        """Generates a landing page for a QR code."""
        data = {"qr_code_id": qr_code_id, "brand_metadata": brand_metadata}
        return self._request("POST", "/generate_landing_page", data=data)

    def trigger_scan_alert(self, qr_code_id: str, location_data: Dict, device_type: str, user_settings: Dict) -> Dict:
        """Triggers a scan alert."""
        data = {"qr_code_id": qr_code_id, "location_data": location_data, "device_type": device_type, "user_settings": user_settings}
        return self._request("POST", "/scan_alert", data=data)

    def push_crm_contact(self, crm_name: str, contact_data: Dict) -> Dict:
        """Pushes contact data to a CRM."""
        data = {"crm_name": crm_name, "contact_data": contact_data}
        return self._request("POST", "/crm_push_contact", data=data)

    def send_payment_webhook(self, user_id: str, transaction_id: str, status: str, amount: float, currency: str, plan_name: Optional[str] = None, signature: str = "mock_signature") -> Dict:
        """Simulates sending a payment status webhook."""
        data = {
            "user_id": user_id,
            "transaction_id": transaction_id,
            "status": status,
            "amount": amount,
            "currency": currency,
            "plan_name": plan_name,
            "signature": signature
        }
        return self._request("POST", "/webhook/payment_status", data=data)

    def get_feature_status(self, feature_name: str) -> Dict:
        """Checks the status of a feature flag."""
        return self._request("GET", f"/feature_status/{feature_name}")

    def export_user_data(self) -> Dict:
        """Exports the current user's data."""
        return self._request("GET", "/users/me/data/export")

    def delete_user_data(self) -> Dict:
        """Deletes the current user's data."""
        return self._request("DELETE", "/users/me/data/delete")

    def get_protected_data(self) -> Dict:
        """Retrieves protected data from the API."""
        return self._request("GET", "/protected_data")

    def inject_chaos(self, scenario_type: str, duration_ms: Optional[int] = None, duration_s: Optional[int] = None, intensity: Optional[float] = None, size_mb: Optional[int] = None, probability: Optional[float] = None) -> Dict:
        """Injects a chaos scenario into the system (admin access required)."""
        data = {k: v for k, v in locals().items() if k not in ['self', 'scenario_type'] and v is not None}
        data["scenario_type"] = scenario_type # Ensure scenario_type is included
        return self._request("POST", "/admin/chaos/inject", data=data)

# Example Usage (for testing)
if __name__ == "__main__":
    BASE_URL = "http://localhost:8000" # Replace with your API base URL
    sdk = ShujaaSDK(BASE_URL)

    print("--- Health Check ---")
    try:
        health_response = sdk.get_health()
        print(f"Health Check: {health_response}")
    except Exception as e:
        print(f"Health Check Failed: {e}")

    print("\n--- User Registration ---")
    try:
        register_response = sdk.register_user("sdk_test_user", "sdk@example.com", "password123")
        print(f"Register User: {register_response}")
    except Exception as e:
        print(f"Register User Failed: {e}")

    print("\n--- Get Token ---")
    try:
        token_response = sdk.get_token("sdk_test_user", "password123")
        print(f"Get Token: {token_response}")
        # Update SDK with the new token for subsequent requests
        sdk.api_key = token_response["access_token"]
        sdk.headers["Authorization"] = f"Bearer {sdk.api_key}"
    except Exception as e:
        print(f"Get Token Failed: {e}")

    if sdk.api_key:
        print("\n--- Get User Profile ---")
        try:
            profile_response = sdk.get_user_profile()
            print(f"User Profile: {profile_response}")
        except Exception as e:
            print(f"Get User Profile Failed: {e}")

        print("\n--- Get User Plan ---")
        try:
            plan_response = sdk.get_user_plan()
            print(f"User Plan: {plan_response}")
        except Exception as e:
            print(f"Get User Plan Failed: {e}")

        print("\n--- Get User Usage ---")
        try:
            usage_response = sdk.get_user_usage()
            print(f"User Usage: {usage_response}")
        except Exception as e:
            print(f"Get User Usage Failed: {e}")

        print("\n--- Generate Video (Example) ---")
        try:
            video_request = {"prompt": "A beautiful Kenyan landscape"}
            video_response = sdk.generate_video(**video_request)
            print(f"Generate Video: {video_response}")
        except Exception as e:
            print(f"Generate Video Failed: {e}")

        print("\n--- Feature Status Check (Example) ---")
        try:
            feature_status = sdk.get_feature_status("new_ui")
            print(f"Feature 'new_ui' status: {feature_status}")
        except Exception as e:
            print(f"Feature Status Check Failed: {e}")

        print("\n--- Export User Data ---")
        try:
            export_response = sdk.export_user_data()
            print(f"Export User Data: {export_response}")
        except Exception as e:
            print(f"Export User Data Failed: {e}")

        print("\n--- Delete User Data (Caution: This will deactivate the user) ---")
        # try:
        #     delete_response = sdk.delete_user_data()
        #     print(f"Delete User Data: {delete_response}")
        # except Exception as e:
        #     print(f"Delete User Data Failed: {e}")
    else:
        print("Skipping authenticated SDK calls as token was not obtained.")