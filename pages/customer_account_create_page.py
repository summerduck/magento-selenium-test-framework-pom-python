"""Module containing CustomerAccountCreatePage class for account creation page interactions."""

import logging
from time import sleep
from selenium.webdriver.common.by import By
from data.users import UserData, User
from pages.base_page import BasePage

# Initialize logger
logger = logging.getLogger(__name__)


class CustomerAccountCreatePage(BasePage):
    """Class for interacting with the customer account creation page."""

    page_url = "/customer/account/create/"

    # Form locators
    FIRSTNAME_INPUT = (By.ID, "firstname")
    LASTNAME_INPUT = (By.ID, "lastname")
    EMAIL_INPUT = (By.ID, "email_address")
    PASSWORD_INPUT = (By.ID, "password")
    PASSWORD_CONFIRM_INPUT = (By.ID, "password-confirmation")

    # Submit button locator
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[title='Create an Account']")

    # Error locators
    FIRSTNAME_ERROR = (By.ID, "firstname-error")
    LASTNAME_ERROR = (By.ID, "lastname-error")
    EMAIL_ERROR = (By.ID, "email_address-error")
    PASSWORD_ERROR = (By.ID, "password-error")
    PASSWORD_CONFIRM_ERROR = (By.ID, "password-confirmation-error")

    # Password strength meter locators
    PASSWORD_STRENGTH_METER = (By.ID, "password-strength-meter")
    PASSWORD_STRENGTH_METER_LABEL = (By.ID, "password-strength-meter-label")
    PASSWORD_ERROR = (By.ID, "password-error")

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
        # Open the page
        logger.info("Opening page: %s", self.customer_account_create_page_url)
        self.driver.get(self.customer_account_create_page_url)

        # Check if the current URL matches the expected URL
        assert self.driver.current_url == self.customer_account_create_page_url
        logger.info("Current URL matches expected URL")

        # Check if the customer account create page class is visible
        page_class = self.driver.find_element(
            "css selector", ".customer-account-create.page-layout-1column"
        )
        assert (
            page_class.is_displayed()
        ), "Customer account create page class is not visible"
        logger.info("Customer account create page class is visible")

    def submit_form(
        self,
    ):
        """
        Submit the registration form.
        """
        logger.info("Submitting registration form")
        self.find(self.SUBMIT_BUTTON).click()
        logger.info("Registration form submitted")

    def get_error_messages(
        self,
    ):
        """
        Get all error messages from the form.
        """
        logger.info("Getting error messages from all form fields")
        self.error_messages = {
            "firstname": self.get_text(self.FIRSTNAME_ERROR),
            "lastname": self.get_text(self.LASTNAME_ERROR),
            "email": self.get_text(self.EMAIL_ERROR),
            "password": self.get_text(self.PASSWORD_ERROR),
            "password_confirm": self.get_text(self.PASSWORD_CONFIRM_ERROR),
        }
        logger.info("Error messages collected: %s", self.error_messages)

    def verify_required_field_error_message(
        self,
        field: str,
        error_message: str = "This is a required field",
    ):
        """
        Verify required field error message for a specific form field.

        Args:
            field (str): Name of the form field to verify required error message for.
                Field name must be one of the following:
                - "firstname"
                - "lastname"
                - "email"
                - "password"
                - "password_confirm"
            error_message (str): Expected error message for the field
        """
        logger.info("Verifying required field error message for %s", field)
        assert (
            error_message in self.error_messages[field]
        ), f"{field.title()} required field error message not displayed"
        logger.info("Required field error message verified for %s", field)

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
            "All required field error messages verified. Error messages: %s",
            self.error_messages,
        )

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

        If user is provided, use the user data
        If firstname, lastname, email, password are provided, use the provided values

        Args:
            user (UserData): User data to fill the form with
            firstname (str): First name to fill the form with, optional
            lastname (str): Last name to fill the form with, optional
            email (str): Email to fill the form with, optional
            password (str): Password to fill the form with, optional
        """
        # If user is provided, use the user data
        if user:
            firstname = user.first_name
            lastname = user.last_name
            email = user.email
            password = user.password

        # Log the values being used to fill the form
        logger.info(
            "Filling registration form with values: %s, %s, %s, %s",
            firstname,
            lastname,
            email,
            password,
        )

        # Fill the form if the values are provided
        if firstname:
            self.send_keys(self.FIRSTNAME_INPUT, firstname)
        if lastname:
            self.send_keys(self.LASTNAME_INPUT, lastname)
        if email:
            self.send_keys(self.EMAIL_INPUT, email)
        if password:
            self.send_keys(self.PASSWORD_INPUT, password)
        if password_confirmation:
            self.send_keys(self.PASSWORD_CONFIRM_INPUT, password_confirmation)
        else:
            self.send_keys(self.PASSWORD_CONFIRM_INPUT, password)

        logger.info("Registration form filled")

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
            case _:
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
        logger.info("Verifying password strength meter")

        sleep(3)
        assert self.get_text(self.PASSWORD_STRENGTH_METER_LABEL) == label
        logger.info("Password strength meter verified")

        password_class = self.__get_password_class(label)
        assert (
            self.find(self.PASSWORD_STRENGTH_METER).get_attribute("class")
            == password_class
        )
        logger.info("Password strength meter class verified")

        if message_type == "error" and error_message:
            assert self.get_text(self.PASSWORD_ERROR) == error_message
            logger.info("Password error message verified")
