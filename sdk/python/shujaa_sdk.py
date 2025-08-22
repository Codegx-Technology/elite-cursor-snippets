import requests
import json
from typing import Optional, Dict, Any, List
from urllib.parse import urljoin
from error_utils import retry_on_exception
from .exceptions import APIError, AuthenticationError, ConnectionError

class ShujaaSDK:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        """Initializes the Shujaa SDK.

        Args:
            base_url: The base URL of the Shujaa Studio API.
            api_key: The API key for authentication.
        """
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
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise AuthenticationError(f"Authentication failed: {e.response.text}")
            elif e.response.status_code == 403:
                raise APIError(e.response.status_code, f"Forbidden: {e.response.text}")
            else:
                raise APIError(e.response.status_code, e.response.text)
        except requests.exceptions.ConnectionError as e:
            raise ConnectionError(f"Connection Error: {e}")
        except requests.exceptions.Timeout as e:
            raise ConnectionError(f"Timeout Error: {e}")
        except requests.exceptions.RequestException as e:
            raise ShujaaSDKException(f"Request Error: {e}")

    def get_health(self) -> Dict:
        """Checks the health of the API.

        Returns:
            A dictionary containing the health status of the API.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
        """
        return self._request("GET", "/health")

    def register_user(self, username: str, email: str, password: str, tenant_name: Optional[str] = "default", idempotency_key: Optional[str] = None) -> Dict:
        """Registers a new user.

        Args:
            username: The username of the new user.
            email: The email of the new user.
            password: The password of the new user.
            tenant_name: The name of the tenant to register the user under.
            idempotency_key: An optional key to ensure the request is idempotent.

        Returns:
            A dictionary containing the new user's information.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
        """
        data = {"username": username, "email": email, "password": password, "tenant_name": tenant_name}
        return self._request("POST", "/register", data=data, idempotency_key=idempotency_key)

    def get_token(self, username: str, password: str) -> Dict:
        """Gets an access token for a user.

        Args:
            username: The username of the user.
            password: The password of the user.

        Returns:
            A dictionary containing the access token.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
        """
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
        """Retrieves the current user's profile.

        Returns:
            A dictionary containing the user's profile information.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
            AuthenticationError: If the user is not authenticated.
        """
        return self._request("GET", "/users/me")

    def update_user_profile(self, email: Optional[str] = None, full_name: Optional[str] = None, bio: Optional[str] = None, idempotency_key: Optional[str] = None) -> Dict:
        """Updates the current user's profile.

        Args:
            email: The new email of the user.
            full_name: The new full name of the user.
            bio: The new bio of the user.
            idempotency_key: An optional key to ensure the request is idempotent.

        Returns:
            A dictionary containing the updated user's profile information.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
            AuthenticationError: If the user is not authenticated.
        """
        data = {k: v for k, v in locals().items() if k not in ['self', 'idempotency_key'] and v is not None}
        return self._request("PUT", "/users/me", data=data, idempotency_key=idempotency_key)

    def get_user_plan(self) -> Dict:
        """Retrieves the current user's plan details.

        Returns:
            A dictionary containing the user's plan details.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
            AuthenticationError: If the user is not authenticated.
        """
        return self._request("GET", "/users/me/plan")

    def get_user_usage(self) -> Dict:
        """Retrieves the current user's usage statistics.

        Returns:
            A dictionary containing the user's usage statistics.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
            AuthenticationError: If the user is not authenticated.
        """
        return self._request("GET", "/users/me/usage")

    def generate_video(self, prompt: str, news_url: Optional[str] = None, script_file: Optional[str] = None, upload_youtube: bool = False, idempotency_key: Optional[str] = None) -> Dict:
        """Generates a video based on a prompt, news URL, or script file.

        Args:
            prompt: The text prompt for video generation.
            news_url: An optional news URL to generate video from.
            script_file: An optional script file for video generation.
            upload_youtube: A boolean indicating whether to upload the video to YouTube.
            idempotency_key: An optional key to ensure the request is idempotent.

        Returns:
            A dictionary containing the video generation status.

        Raises:
            APIError: If the API returns an error.
            ConnectionError: If there is a connection error.
            AuthenticationError: If the user is not authenticated.
        """
        data = {"prompt": prompt, "news_url": news_url, "script_file": script_file, "upload_youtube": upload_youtube}
        return self._request("POST", "/generate_video", data=data, idempotency_key=idempotency_key)

    def batch_generate_video(self, requests: List[Dict], idempotency_key: Optional[str] = None) -> Dict:
        """Generates multiple videos in a batch."""
        data = {"requests": requests}
        return self._request("POST", "/batch_generate_video", data=data, idempotency_key=idempotency_key)

    def generate_landing_page(self, qr_code_id: str, brand_metadata: Dict, idempotency_key: Optional[str] = None) -> Dict:
        """Generates a landing page for a QR code."""
        data = {"qr_code_id": qr_code_id, "brand_metadata": brand_metadata}
        return self._request("POST", "/generate_landing_page", data=data, idempotency_key=idempotency_key)

    def trigger_scan_alert(self, qr_code_id: str, location_data: Dict, device_type: str, user_settings: Dict, idempotency_key: Optional[str] = None) -> Dict:
        """Triggers a scan alert."""
        data = {"qr_code_id": qr_code_id, "location_data": location_data, "device_type": device_type, "user_settings": user_settings}
        return self._request("POST", "/scan_alert", data=data, idempotency_key=idempotency_key)

    def push_crm_contact(self, crm_name: str, contact_data: Dict, idempotency_key: Optional[str] = None) -> Dict:
        """Pushes contact data to a CRM."""
        data = {"crm_name": crm_name, "contact_data": contact_data}
        return self._request("POST", "/crm_push_contact", data=data, idempotency_key=idempotency_key)

    def send_payment_webhook(self, user_id: str, transaction_id: str, status: str, amount: float, currency: str, plan_name: Optional[str] = None, signature: str = "mock_signature", idempotency_key: Optional[str] = None) -> Dict:
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
        return self._request("POST", "/webhook/payment_status", data=data, idempotency_key=idempotency_key)

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

    def inject_chaos(self, scenario_type: str, duration_ms: Optional[int] = None, duration_s: Optional[int] = None, intensity: Optional[float] = None, size_mb: Optional[int] = None, probability: Optional[float] = None, idempotency_key: Optional[str] = None) -> Dict:
        """Injects a chaos scenario into the system (admin access required)."""
        data = {k: v for k, v in locals().items() if k not in ['self', 'scenario_type', 'idempotency_key'] and v is not None}
        data["scenario_type"] = scenario_type # Ensure scenario_type is included
        return self._request("POST", "/admin/chaos/inject", data=data, idempotency_key=idempotency_key)

    def get_custom_domain(self) -> Dict:
        """Retrieves the custom domain and TLS status for the current tenant."""
        return self._request("GET", "/api/custom-domain")

    def set_custom_domain(self, domain: str, idempotency_key: Optional[str] = None) -> Dict:
        """Sets the custom domain for the current tenant."""
        data = {"domain": domain}
        return self._request("POST", "/api/custom-domain", data=data, idempotency_key=idempotency_key)

    def delete_custom_domain(self) -> Dict:
        """Deletes the custom domain for the current tenant."""
        return self._request("DELETE", "/api/custom-domain")

# Example Usage (for testing)
if __name__ == "__main__":
    import os

    BASE_URL = os.getenv("SHUJAA_BASE_URL", "http://localhost:8000")
    SDK_TEST_USERNAME = os.getenv("SDK_TEST_USERNAME")
    SDK_TEST_PASSWORD = os.getenv("SDK_TEST_PASSWORD")

    if not all([SDK_TEST_USERNAME, SDK_TEST_PASSWORD]):
        print("Please set SDK_TEST_USERNAME and SDK_TEST_PASSWORD environment variables to run the SDK tests.")
    else:
        sdk = ShujaaSDK(BASE_URL)

        print("--- Health Check ---")
        try:
            health_response = sdk.get_health()
            print(f"Health Check: {health_response}")
        except Exception as e:
            print(f"Health Check Failed: {e}")

        print("\n--- User Registration ---")
        try:
            register_response = sdk.register_user(SDK_TEST_USERNAME, "sdk@example.com", SDK_TEST_PASSWORD)
            print(f"Register User: {register_response}")
        except Exception as e:
            print(f"Register User Failed: {e}")

        print("\n--- Get Token ---")
        try:
            token_response = sdk.get_token(SDK_TEST_USERNAME, SDK_TEST_PASSWORD)
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
