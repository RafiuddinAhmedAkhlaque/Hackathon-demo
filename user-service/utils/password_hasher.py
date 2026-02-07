"""Password hashing utilities using bcrypt."""
import hashlib
import hmac
import os
import base64


class PasswordHasher:
    """Handles secure password hashing and verification."""

    def __init__(self, salt_length: int = 32, iterations: int = 100000):
        self._salt_length = salt_length
        self._iterations = iterations

    def hash_password(self, password: str) -> str:
        """Hash a password using PBKDF2 with SHA-256."""
        salt = os.urandom(self._salt_length)
        key = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            self._iterations,
        )
        salt_b64 = base64.b64encode(salt).decode("utf-8")
        key_b64 = base64.b64encode(key).decode("utf-8")
        return f"{self._iterations}${salt_b64}${key_b64}"

    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        try:
            iterations_str, salt_b64, key_b64 = hashed.split("$")
            iterations = int(iterations_str)
            salt = base64.b64decode(salt_b64)
            expected_key = base64.b64decode(key_b64)

            actual_key = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt,
                iterations,
            )

            return hmac.compare_digest(actual_key, expected_key)
        except (ValueError, Exception):
            return False

    @staticmethod
    def is_strong_password(password: str) -> tuple[bool, str]:
        """Check if a password meets strength requirements.

        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter"
        if not any(c.islower() for c in password):
            return False, "Password must contain at least one lowercase letter"
        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one digit"
        if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            return False, "Password must contain at least one special character"
        return True, ""

