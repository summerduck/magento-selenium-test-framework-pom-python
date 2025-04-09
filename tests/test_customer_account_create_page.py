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
        Test that appropriate error messages are displayed
        when submitting form with empty required fields.
        """
        customer_account_create_page.open_page()
        customer_account_create_page.is_page_opened()
        customer_account_create_page.submit_form()
        customer_account_create_page.get_error_messages()
        customer_account_create_page.verify_all_required_field_error_messages()

    @mark.account_creation
    def test_create_customer_account(
        self,
        customer_account_create_page,
    ):
        """
        Test to check if the customer account creation page is opened.
        """
        customer_account_create_page.open_page()
        customer_account_create_page.is_page_opened()
        customer_account_create_page.fill_form(user=User.random())
        customer_account_create_page.submit_form()
        customer_account_create_page.verify_account_creation()
