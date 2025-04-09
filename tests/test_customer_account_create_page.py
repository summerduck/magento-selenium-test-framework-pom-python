"""Module containing tests for the customer account creation page."""

from pytest import mark


@mark.smoke
def test_open_customer_account_create_page(customer_account_create_page):
    """Test to check if the customer account creation page is opened."""
    customer_account_create_page.open_page()
    customer_account_create_page.is_page_opened()


def test_create_customer_account(customer_account_create_page):
    """Test to check if the customer account creation page is opened."""
    customer_account_create_page.open_page()
    customer_account_create_page.is_page_opened()


@mark.validation
def test_empty_fields_validation(customer_account_create_page):
    """Test form validation with all empty fields."""
    # Open the page
    customer_account_create_page.open_page()
    customer_account_create_page.is_page_opened()

    # Submit the form without filling any fields
    customer_account_create_page.submit_form()

    # Get error messages
    error_messages = customer_account_create_page.get_error_messages()

    # Verify error messages for each field
    assert (
        "This is a required field" in error_messages["firstname"]
    ), "First name error message not displayed"
    assert (
        "This is a required field" in error_messages["lastname"]
    ), "Last name error message not displayed"
    assert (
        "This is a required field" in error_messages["email"]
    ), "Email error message not displayed"
    assert (
        "This is a required field" in error_messages["password"]
    ), "Password error message not displayed"
    assert (
        "This is a required field" in error_messages["password_confirm"]
    ), "Password confirmation error message not displayed"
