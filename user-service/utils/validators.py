"""Input validation utilities."""
import re
from typing import Tuple


def validate_email(email: str) -> Tuple[bool, str]:
    """Validate an email address format.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email or not email.strip():
        return False, "Email address is required"

    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        return False, "Invalid email address format"

    if len(email) > 254:
        return False, "Email address is too long"

    return True, ""


def validate_username(username: str) -> Tuple[bool, str]:
    """Validate a username.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username or not username.strip():
        return False, "Username is required"

    if len(username) < 3:
        return False, "Username must be at least 3 characters long"

    if len(username) > 30:
        return False, "Username must be at most 30 characters long"

    pattern = r'^[a-zA-Z0-9_-]+$'
    if not re.match(pattern, username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, ""


def validate_phone(phone: str) -> Tuple[bool, str]:
    """Validate a phone number.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not phone:
        return True, ""  # Phone is optional

    cleaned = re.sub(r'[\s\-\(\)\.]', '', phone)

    if not re.match(r'^\+?[0-9]{10,15}$', cleaned):
        return False, "Invalid phone number format"

    return True, ""


def validate_postal_code(postal_code: str, country: str = "US") -> Tuple[bool, str]:
    """Validate a postal code based on country.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not postal_code or not postal_code.strip():
        return False, "Postal code is required"

    patterns = {
        "US": r'^\d{5}(-\d{4})?$',
        "CA": r'^[A-Za-z]\d[A-Za-z]\s?\d[A-Za-z]\d$',
        "UK": r'^[A-Za-z]{1,2}\d[A-Za-z\d]?\s?\d[A-Za-z]{2}$',
        "DE": r'^\d{5}$',
        "FR": r'^\d{5}$',
    }

    pattern = patterns.get(country.upper())
    if pattern and not re.match(pattern, postal_code):
        return False, f"Invalid postal code format for {country}"

    return True, ""


def validate_name(name: str, field_name: str = "Name") -> Tuple[bool, str]:
    """Validate a person's name.

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name or not name.strip():
        return False, f"{field_name} is required"

    if len(name.strip()) < 1:
        return False, f"{field_name} must be at least 1 character long"

    if len(name) > 100:
        return False, f"{field_name} must be at most 100 characters long"

    if re.search(r'[<>{}[\]\\]', name):
        return False, f"{field_name} contains invalid characters"

    return True, ""

