"""JWT token management utilities."""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import hashlib
import hmac
import base64
import json
import os


# Secret key for signing tokens - in production, load from environment
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24


class TokenManager:
    """Handles JWT token creation and validation."""

    def __init__(self, secret_key: str = SECRET_KEY, expire_hours: int = ACCESS_TOKEN_EXPIRE_HOURS):
        self._secret_key = secret_key
        self._expire_hours = expire_hours

    def create_access_token(self, user_id: str, extra_claims: Optional[Dict[str, Any]] = None) -> str:
        """Create a JWT access token for a user."""
        now = datetime.utcnow()
        payload = {
            "user_id": user_id,
            "iat": now.isoformat(),
            "exp": (now + timedelta(hours=self._expire_hours)).isoformat(),
        }
        if extra_claims:
            payload.update(extra_claims)

        return self._encode_token(payload)

    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode and validate a JWT token."""
        try:
            payload = self._decode_token(token)
            if not payload:
                return None

            exp = datetime.fromisoformat(payload["exp"])
            if datetime.utcnow() > exp:
                return None

            return payload
        except (KeyError, ValueError, Exception):
            return None

    def get_user_id_from_token(self, token: str) -> Optional[str]:
        """Extract user_id from a valid token."""
        payload = self.decode_token(token)
        if payload:
            return payload.get("user_id")
        return None

    def _encode_token(self, payload: dict) -> str:
        """Simple HMAC-SHA256 based token encoding."""
        header = base64.urlsafe_b64encode(
            json.dumps({"alg": "HS256", "typ": "JWT"}).encode()
        ).decode().rstrip("=")

        payload_encoded = base64.urlsafe_b64encode(
            json.dumps(payload).encode()
        ).decode().rstrip("=")

        message = f"{header}.{payload_encoded}"
        signature = hmac.new(
            self._secret_key.encode(),
            message.encode(),
            hashlib.sha256,
        ).digest()
        sig_encoded = base64.urlsafe_b64encode(signature).decode().rstrip("=")

        return f"{header}.{payload_encoded}.{sig_encoded}"

    def _decode_token(self, token: str) -> Optional[dict]:
        """Decode and verify a token."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return None

            header_part, payload_part, sig_part = parts

            # Verify signature
            message = f"{header_part}.{payload_part}"
            expected_sig = hmac.new(
                self._secret_key.encode(),
                message.encode(),
                hashlib.sha256,
            ).digest()
            expected_encoded = base64.urlsafe_b64encode(expected_sig).decode().rstrip("=")

            if not hmac.compare_digest(sig_part, expected_encoded):
                return None

            # Decode payload
            padding = 4 - len(payload_part) % 4
            if padding != 4:
                payload_part += "=" * padding

            payload = json.loads(base64.urlsafe_b64decode(payload_part))
            return payload
        except Exception:
            return None

