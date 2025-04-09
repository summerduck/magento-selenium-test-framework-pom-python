"""Module containing BasePage class for base page interactions."""

from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """Base class for all page objects."""

    base_url = "https://magento.softwaretestingboard.com"
    page_url = None

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def open_page(self):
        """Open the page specified by the URL."""
        if self.page_url:
            self.driver.get(f"{self.base_url}{self.page_url}")
        else:
            raise NotImplementedError("Page can not be opened for this page class")

    def find(self, locator: tuple):
        """Find an element on the page."""
        return self.driver.find_element(*locator)

    def find_all(self, locator: tuple):
        """Find all elements on the page."""
        return self.driver.find_elements(*locator)
