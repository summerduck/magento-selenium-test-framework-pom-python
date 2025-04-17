"""Module containing CustomerAccountCreatePage class for account creation page interactions."""

import logging
from time import sleep
from selenium.webdriver.common.keys import Keys
from data.users import UserData, User
from pages.base_page import BasePage
from pages.locators import CustomerAccountCreatePageLocators as loc

# Initialize logger
logger = logging.getLogger(__name__)


class CustomerAccountCreatePage(BasePage):
    """Class for interacting with the customer account creation page."""

    page_url = "/customer/account/create/"

    def __init__(
        self,
        driver,
    ):
        """
        Initialize the CustomerAccountCreatePage instance.
        """
        super().__init__(driver)
        self.error_messages = {}
        self.customer_account_create_page_url = f"{self.base_url}{self.page_url}"

    def open_page(
        self,
    ):
        """
        Open the customer account creation page.
        """
        logger.info(
            "Navigating to Account Creation page at: %s",
            self.customer_account_create_page_url,
        )
        self.goto(self.customer_account_create_page_url)

        # Verify URL
        assert self.driver.current_url == self.customer_account_create_page_url, (
            f"Expected URL: {self.customer_account_create_page_url}, "
            f"but got: {self.driver.current_url}"
        )
        logger.info(
            "✓ Confirmed: Current URL matches expected Account Creation page URL"
        )

        # Verify page layout
        page_class = self.driver.find_element(
            "css selector", ".customer-account-create.page-layout-1column"
        )
        assert (
            page_class.is_displayed()
        ), "Account Creation page layout elements are not visible"
        logger.info("✓ Confirmed: Account Creation page layout is properly displayed")

    def submit_form(
        self,
    ):
        """
        Submit the registration form.
        """
        logger.info("Submitting customer account registration form")
        self.find(loc.SUBMIT_BUTTON).click()
        logger.info("✓ Registration form submitted successfully")

    def get_error_messages(
        self,
    ):
        """
        Get all error messages from the form.
        """
        logger.info("Collecting error messages from all registration form fields")
        self.error_messages = {
            "firstname": self.get_text(loc.FIRSTNAME_ERROR),
            "lastname": self.get_text(loc.LASTNAME_ERROR),
            "email": self.get_text(loc.EMAIL_ERROR),
            "password": self.get_text(loc.PASSWORD_ERROR),
            "password_confirm": self.get_text(loc.PASSWORD_CONFIRM_ERROR),
        }
        logger.debug("Collected error messages: %s", self.error_messages)
        logger.info("✓ Form validation messages retrieved successfully")

    def verify_required_field_error_message(
        self,
        field: str,
        error_message: str = "This is a required field",
    ):
        """
        Verify required field error message for a specific form field.
        """
        logger.info("Verifying required field error message for field: '%s'", field)
        assert error_message in self.error_messages[field], (
            f"Expected error message '{error_message}' not found for {field} field. "
            f"Actual message: {self.error_messages[field]}"
        )
        logger.info(
            "✓ Confirmed: Required field error message verified for '%s'", field
        )

    def verify_all_required_field_error_messages(
        self,
    ):
        """
        Verify required field error messages for all form fields.
        """
        logger.info(
            "Verifying required field error messages for all registration form fields"
        )
        fields = ["firstname", "lastname", "email", "password", "password_confirm"]
        for field in fields:
            self.verify_required_field_error_message(field)
        logger.info(
            "✓ Confirmed: All required field error messages verified successfully"
        )
        logger.debug("Error messages state: %s", self.error_messages)

    def fill_firstname(
        self,
        firstname: str | None = None,
    ):
        """
        Fill the firstname field with the provided value.
        """
        if firstname:
            logger.info("Filling first name field with: '%s'", firstname)
            self.send_keys(loc.FIRSTNAME_INPUT, firstname)

    def fill_lastname(
        self,
        lastname: str | None = None,
    ):
        """
        Fill the lastname field with the provided value.
        """
        if lastname:
            logger.info("Filling last name field with: '%s'", lastname)
            self.send_keys(loc.LASTNAME_INPUT, lastname)

    def fill_email(
        self,
        email: str | None = None,
    ):
        """
        Fill the email field with the provided value.
        """
        if email:
            logger.info("Filling email field with: '%s'", email)
            self.send_keys(loc.EMAIL_INPUT, email)

    def fill_password(
        self,
        password: str | None = None,
    ):
        """
        Fill the password field with the provided value.
        """
        if password:
            logger.info(
                "Filling password field"
            )  # Not logging actual password for security
            self.send_keys(loc.PASSWORD_INPUT, password)
            self.send_keys(loc.PASSWORD_INPUT, Keys.ENTER)

    def fill_password_confirmation(
        self,
        password_confirmation: str | None = None,
    ):
        """
        Fill the password confirmation field with the provided value.
        """
        if password_confirmation:
            logger.info(
                "Filling password confirmation field"
            )  # Not logging actual password for security
            self.send_keys(loc.PASSWORD_CONFIRM_INPUT, password_confirmation)

    def fill_form(
        self,
        user: UserData | None = None,
        firstname: str | None = None,
        lastname: str | None = None,
        email: str | None = None,
        password: str | None = None,
        password_confirmation: str | None = None,
    ):
        """
        Fill the registration form with the provided values.
        """
        logger.info("Starting to fill customer registration form")

        # If user is provided, use the user data
        if user:
            firstname = user.first_name
            lastname = user.last_name
            email = user.email
            password = user.password
            logger.info("Using provided UserData object for form filling")

        # If password_confirmation is not provided, use the password
        password_confirmation = (
            password if password_confirmation is None else password_confirmation
        )

        # Fill the form if the values are provided
        self.fill_firstname(firstname)
        self.fill_lastname(lastname)
        self.fill_email(email)
        self.fill_password(password)
        self.fill_password_confirmation(password_confirmation)

        logger.info("✓ Registration form filled successfully")

    def __get_password_class(self, label: str) -> str:
        """
        Get the class of the password strength meter based on the label.
        """
        match label:
            case "Weak":
                return "password-weak"
            case "Strong":
                return "password-strong"
            case "Very Strong":
                return "password-very-strong"
            case "No Password":
                return "password-none"
            case _:
                logger.error("Invalid password strength label provided: %s", label)
                raise ValueError(f"Invalid password strength label: {label}")

    def verify_password_strength_meter(
        self,
        label: str,
        message_type: str,
        error_message: str | None = None,
    ):
        """
        Verify the password strength meter.
        """
        logger.info(
            "Verifying password strength meter with expected label: '%s'", label
        )
        self.wait_for_element(loc.PASSWORD_STRENGTH_METER)

        # Verify the password strength meter label
        actual_label = self.get_text(loc.PASSWORD_STRENGTH_METER_LABEL)
        assert actual_label == label, (
            f"Password strength meter label mismatch. "
            f"Expected: '{label}', but got: '{actual_label}'"
        )
        logger.info("✓ Confirmed: Password strength meter label matches expected value")

        # Verify the password strength meter class
        password_class = self.__get_password_class(label)
        actual_class = self.find(loc.PASSWORD_STRENGTH_METER).get_attribute("class")
        assert actual_class == password_class, (
            f"Password strength meter class mismatch. "
            f"Expected: '{password_class}', but got: '{actual_class}'"
        )
        logger.info("✓ Confirmed: Password strength meter class matches expected value")

        # Verify the password error message if applicable
        if message_type == "error" and error_message:
            actual_error = self.get_text(loc.PASSWORD_ERROR)
            assert actual_error == error_message, (
                f"Password error message mismatch. "
                f"Expected: '{error_message}', but got: '{actual_error}'"
            )
            logger.info("✓ Confirmed: Password error message matches expected value")
