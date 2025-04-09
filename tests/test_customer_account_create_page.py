"""Module containing tests for the customer account creation page."""

from pytest import mark
from data.enums import User


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

    @mark.validation
    def test_email_validation(
        self,
        customer_account_create_page,
    ):
        """
        Email Validation:
        Test invalid email formats (missing @, no domain, etc.)
        Test valid email format
        """
        pass

    @mark.parametrize(
        "password,label,message_type,error_message",
        [
            ("Password123!", "Very Strong", "success", None),
            ("Password123", "Strong", "success", None),
            (
                "password123",
                "Weak",
                "error",
                "Minimum of different classes of characters in password is 3. Classes of characters: Lower Case, Upper Case, Digits, Special Characters.",
            ),
            (None, "No Password", "error", None),
        ],
    )
    @mark.validation
    def test_password_strength(
        self,
        customer_account_create_page,
        password,
        label,
        message_type,
        error_message,
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
        customer_account_create_page.fill_form(password=password)
        customer_account_create_page.verify_password_strength_meter(
            label=label,
            message_type=message_type,
            error_message=error_message,
        )

    @mark.validation
    @mark.parametrize(
        "password,confirmation,expected_error",
        [
            ("Password123!", "Password123!", None),
            ("Password123!", "password123!", "Please enter the same value again."),
        ],
    )
    def test_password_confirmation_match(
        self,
        customer_account_create_page,
        password,
        confirmation,
        expected_error,
    ):
        """
        Password Confirmation Match: Test with matching and non-matching password confirmation
        """
        pass

    @mark.ui_ux
    def test_password_visibility_toggle(
        self,
        customer_account_create_page,
    ):
        """
        Password Visibility Toggle: Test the "Show Password" checkbox functionality
        """
        pass

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

    @mark.account_creation
    def test_create_customer_account_duplicate_account(
        self,
        customer_account_create_page,
    ):
        """
        Duplicate Account: Try registering with an email that already exists
        """
        pass
