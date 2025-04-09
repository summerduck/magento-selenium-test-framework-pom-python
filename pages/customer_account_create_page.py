"""Module containing CustomerAccountCreatePage class for account creation page interactions."""

from pages.base_page import BasePage
from selenium.webdriver.common.by import By


class CustomerAccountCreatePage(BasePage):
    """Class for interacting with the customer account creation page."""

    page_url = "/customer/account/create/"

    # Form locators
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[title='Create an Account']")
    FIRSTNAME_ERROR = (By.ID, "firstname-error")
    LASTNAME_ERROR = (By.ID, "lastname-error")
    EMAIL_ERROR = (By.ID, "email_address-error")
    PASSWORD_ERROR = (By.ID, "password-error")
    PASSWORD_CONFIRM_ERROR = (By.ID, "password-confirmation-error")

    def __init__(self, driver):
        """Initialize the CustomerAccountCreatePage instance."""
        super().__init__(driver)

    def open_page(self):
        """Open the customer account creation page."""
        self.driver.get(f"{self.base_url}{self.page_url}")

    def is_page_opened(self):
        """Check if the customer account creation page is opened"""
        assert self.driver.current_url == f"{self.base_url}{self.page_url}"
        page_class = self.driver.find_element(
            "css selector", ".customer-account-create.page-layout-1column"
        )
        assert (
            page_class.is_displayed()
        ), "Customer account create page class is not visible"

    def submit_form(self):
        """Submit the registration form."""
        self.find(self.SUBMIT_BUTTON).click()

    def get_error_messages(self):
        """Get all error messages from the form."""
        error_messages = {
            "firstname": self.find(self.FIRSTNAME_ERROR).text,
            "lastname": self.find(self.LASTNAME_ERROR).text,
            "email": self.find(self.EMAIL_ERROR).text,
            "password": self.find(self.PASSWORD_ERROR).text,
            "password_confirm": self.find(self.PASSWORD_CONFIRM_ERROR).text,
        }
        return error_messages
