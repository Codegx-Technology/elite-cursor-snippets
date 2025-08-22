class ShujaaSDKException(Exception):
    """Base exception class for the Shujaa SDK."""
    pass

class APIError(ShujaaSDKException):
    """Raised for API errors."""
    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")

class AuthenticationError(ShujaaSDKException):
    """Raised for authentication errors."""
    pass

class ConnectionError(ShujaaSDKException):
    """Raised for connection errors."""
    pass
