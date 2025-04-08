"""Module containing EcoFriendlyPage class for eco-friendly page interactions."""

from pages.base_page import BasePage


class EcoFriendlyPage(BasePage):
    """Class for interacting with the eco-friendly page."""

    def __init__(self, driver):
        """Initialize the EcoFriendlyPage instance."""
        super().__init__(driver)

    def open_page(self):
        """Open the eco-friendly page."""
        self.driver.get("https://magento.softwaretestingboard.com/eco-friendly.html")
