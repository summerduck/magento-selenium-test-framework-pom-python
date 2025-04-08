"""Module containing CustomerAccountCreatePage class for account creation page interactions."""

from pages.base_page import BasePage


class CustomerAccountCreatePage(BasePage):
    """Class for interacting with the customer account creation page."""

    def __init__(self, driver):
        """Initialize the CustomerAccountCreatePage instance."""
        super().__init__(driver)

    def open_page(self):
        """Open the customer account creation page."""
        self.driver.get(
            "https://magento.softwaretestingboard.com/customer/account/create/"
        )
