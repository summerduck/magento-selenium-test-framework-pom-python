"""Module containing BasePage class for base page interactions."""


class BasePage:
    """Base class for all page objects."""

    def __init__(self, driver):
        """Initialize the BasePage instance."""
        self.driver = driver

    def open_page(self, url):
        """Open the page specified by the URL."""
        self.driver.get(url)
