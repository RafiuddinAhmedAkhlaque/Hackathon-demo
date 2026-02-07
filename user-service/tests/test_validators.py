"""Tests for validation utilities."""
import pytest
from utils.validators import (
    validate_email,
    validate_username,
    validate_phone,
    validate_postal_code,
    validate_name,
)
from utils.password_hasher import PasswordHasher


class TestEmailValidation:
    def test_valid_email(self):
        valid, msg = validate_email("user@example.com")
        assert valid is True

    def test_invalid_email_no_at(self):
        valid, msg = validate_email("userexample.com")
        assert valid is False

    def test_invalid_email_no_domain(self):
        valid, msg = validate_email("user@")
        assert valid is False

    def test_empty_email(self):
        valid, msg = validate_email("")
        assert valid is False

    def test_email_too_long(self):
        valid, msg = validate_email("a" * 250 + "@example.com")
        assert valid is False


class TestUsernameValidation:
    def test_valid_username(self):
        valid, msg = validate_username("john_doe")
        assert valid is True

    def test_username_too_short(self):
        valid, msg = validate_username("ab")
        assert valid is False

    def test_username_too_long(self):
        valid, msg = validate_username("a" * 31)
        assert valid is False

    def test_username_invalid_chars(self):
        valid, msg = validate_username("john doe!")
        assert valid is False

    def test_username_with_hyphens(self):
        valid, msg = validate_username("john-doe")
        assert valid is True


class TestPhoneValidation:
    def test_valid_phone(self):
        valid, msg = validate_phone("+1234567890")
        assert valid is True

    def test_empty_phone(self):
        valid, msg = validate_phone("")
        assert valid is True  # Phone is optional

    def test_none_phone(self):
        valid, msg = validate_phone(None)
        assert valid is True

    def test_invalid_phone(self):
        valid, msg = validate_phone("abc")
        assert valid is False


class TestPostalCodeValidation:
    def test_valid_us_zip(self):
        valid, msg = validate_postal_code("62701", "US")
        assert valid is True

    def test_valid_us_zip_plus4(self):
        valid, msg = validate_postal_code("62701-1234", "US")
        assert valid is True

    def test_invalid_us_zip(self):
        valid, msg = validate_postal_code("ABC", "US")
        assert valid is False

    def test_empty_postal_code(self):
        valid, msg = validate_postal_code("", "US")
        assert valid is False


class TestNameValidation:
    def test_valid_name(self):
        valid, msg = validate_name("John")
        assert valid is True

    def test_empty_name(self):
        valid, msg = validate_name("")
        assert valid is False

    def test_name_with_invalid_chars(self):
        valid, msg = validate_name("<script>alert</script>")
        assert valid is False

    def test_name_too_long(self):
        valid, msg = validate_name("A" * 101)
        assert valid is False


class TestPasswordHasher:
    def test_hash_and_verify(self):
        hasher = PasswordHasher()
        hashed = hasher.hash_password("MyPassword123!")
        assert hasher.verify_password("MyPassword123!", hashed) is True

    def test_verify_wrong_password(self):
        hasher = PasswordHasher()
        hashed = hasher.hash_password("MyPassword123!")
        assert hasher.verify_password("WrongPassword!", hashed) is False

    def test_strong_password(self):
        valid, msg = PasswordHasher.is_strong_password("SecurePass1!")
        assert valid is True

    def test_weak_password_short(self):
        valid, msg = PasswordHasher.is_strong_password("Ab1!")
        assert valid is False

    def test_weak_password_no_upper(self):
        valid, msg = PasswordHasher.is_strong_password("securepass1!")
        assert valid is False

    def test_weak_password_no_digit(self):
        valid, msg = PasswordHasher.is_strong_password("SecurePass!")
        assert valid is False

    def test_weak_password_no_special(self):
        valid, msg = PasswordHasher.is_strong_password("SecurePass1")
        assert valid is False

