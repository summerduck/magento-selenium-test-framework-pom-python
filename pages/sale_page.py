"""Module containing SalePage class for sale page interactions."""

from pages.base_page import BasePage


class SalePage(BasePage):
    """Class for interacting with the sale page."""

    def __init__(self, driver):
        """Initialize the SalePage instance."""
        super().__init__(driver)

    def open_page(self):
        """Open the sale page."""
        self.driver.get("https://magento.softwaretestingboard.com/sale.html")
