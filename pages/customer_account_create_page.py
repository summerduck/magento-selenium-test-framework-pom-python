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
        logger.info("Opening page: %s%s", self.base_url, self.page_url)
        self.driver.get(self.customer_account_create_page_url)

    def is_page_opened(
        self,
    ):
        """
        Check if the customer account creation page is opened
        """
        logger.info("Checking if customer account creation page is opened")

        # Check if the current URL matches the expected URL
        assert self.driver.current_url == self.customer_account_create_page_url
        logger.debug("Current URL matches expected URL")

        # Check if the customer account create page class is visible
        page_class = self.driver.find_element(
            "css selector", ".customer-account-create.page-layout-1column"
        )
        assert (
            page_class.is_displayed()
        ), "Customer account create page class is not visible"
        logger.debug("Customer account create page class is visible")

    def submit_form(
        self,
    ):
        """
        Submit the registration form.
        """
        logger.info("Submitting registration form")
        self.find(self.SUBMIT_BUTTON).click()
        logger.debug("Registration form submitted")

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
        logger.debug("Error messages collected: %s", self.error_messages)

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
        logger.debug("Required field error message verified for %s", field)

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
        logger.debug(
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
    ):
        """
        Fill the registration form with the provided values.
        """
        if user:
            firstname = user.first_name
            lastname = user.last_name
            email = user.email
            password = user.password

        logger.info(
            "Filling registration form with values: %s, %s, %s, %s",
            firstname,
            lastname,
            email,
            password,
        )

        self.send_keys(self.FIRSTNAME_INPUT, firstname)
        self.send_keys(self.LASTNAME_INPUT, lastname)
        self.send_keys(self.EMAIL_INPUT, email)
        self.send_keys(self.PASSWORD_INPUT, password)
        self.send_keys(self.PASSWORD_CONFIRM_INPUT, password)
        logger.debug("Registration form filled")

    def verify_account_creation(
        self,
    ):
        """
        Verify account creation.
        """
        logger.info("Verifying account creation")
        sleep(10)
        success_message = self.driver.find_element(
            By.XPATH,
            "//div[contains(text(), 'Thank you for registering with Main Website Store.')]",
        )
        self.wait_for_element(success_message)
        assert success_message.is_displayed(), "Success message is not displayed"
        logger.debug("Account creation success message verified")
