"""Module containing tests for the customer account creation page."""

import logging
from pytest import mark
from data.enums import User

logger = logging.getLogger(__name__)


class CustomerAccountCreatePageTest:
    """Test class for customer account creation page functionality."""

    @mark.validation
    def test_validate_required_fields_error_messages(
        self,
        customer_account_create_page,
    ):
        """
        Empty Field Validation: Submit the form with all empty fields and verify error messages
        Required Fields: Verify all required fields show appropriate validation messages
        """
        customer_account_create_page.open_page()
        customer_account_create_page.submit_form()
        customer_account_create_page.get_error_messages()
        customer_account_create_page.verify_all_required_field_error_messages()

    @mark.account_creation
    def test_create_customer_account_successful_registration(
        self,
        customer_account_create_page,
        customer_account_page,
    ):
        """
        Successful Registration: Complete form with valid data and verify account creation
        """
        customer_account_create_page.open_page()
        customer_account_create_page.fill_form(user=User.random())
        customer_account_create_page.submit_form()
        customer_account_page.verify_account_creation()

    @mark.parametrize(
        "password,label,message_type,error_message",
        [
            ("Password123!", "Very Strong", "success", ""),
            ("Password123", "Very Strong", "success", ""),
            (
                "password123",
                "Weak",
                "error",
                "Minimum of different classes of characters in password is 3. Classes of characters: Lower Case, Upper Case, Digits, Special Characters.",
            ),
            (None, "No Password", "error", ""),
        ],
    )
    @mark.validation
    def test_password_strength(
        self,
        customer_account_create_page,
        password: str,
        label: str,
        message_type: str,
        error_message: str,
    ):
        """
        Password Strength Tests:
        - Basic length requirements
        - Character class requirements (lowercase, uppercase, digits, special chars)
        - Various character combinations
        - Strong password patterns
        - Edge cases and invalid inputs

        Args:
            password (str): The password to test
            label (str): The expected label text. Very Strong, Strong, Weak, No Password
            type (str): The expected type of the password strength meter
        """
        customer_account_create_page.open_page()
        customer_account_create_page.fill_form(user=User.with_custom_password(password))
        customer_account_create_page.verify_password_strength_meter(
            label=label,
            message_type=message_type,
            error_message=error_message,
        )
