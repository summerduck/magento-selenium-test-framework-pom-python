"""Module containing BasePage class for base page interactions."""

import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize logger
logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects."""

    base_url = "https://magento.softwaretestingboard.com"
    page_url = None

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Navigation methods
    def goto(self, url: str):
        """Open the page specified by the URL."""
        if self.page_url:
            self.driver.get(f"{self.base_url}{self.page_url}")
        else:
            raise NotImplementedError("Page can not be opened for this page class")

    def wait_for_page_load(self):
        """Wait for page to load."""
        logger.info("Waiting for page to load")
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

    def reload(self):
        """Reload the current page"""
        self.driver.refresh()
        return self

    def back(self):
        """Navigate back in history"""
        self.driver.back()
        return self

    def forward(self):
        """Navigate forward in history"""
        self.driver.forward()
        return self

    def title(self):
        """Get page title"""
        return self.driver.title

    def url(self):
        """Get current URL"""
        return self.driver.current_url

    # Actions
    def click(self, locator):
        """Click on element."""
        logger.info("Clicking element with locator: %s", locator)
        self.wait_for_element(locator).click()

    def find(self, locator: tuple):
        """Find an element on the page."""
        return self.driver.find_element(*locator)

    def find_all(self, locator: tuple):
        """Find all elements on the page."""
        return self.driver.find_elements(*locator)

    # Assertions
    def expect_to_be_visible(self, locator):
        """Check if element is visible on the page."""
        logger.info("Checking if element with locator: %s is visible", locator)
        element = self.wait.until(EC.visibility_of_element_located(locator))
        assert (
            element is not None
        ), f"Element with locator {locator} not found or not visible"

    def expect_to_have_text(self, locator, text):
        """Check if element has text."""
        logger.info("Checking if element with locator: %s has text: %s", locator, text)
        assert self.wait.until(EC.text_to_be_present_in_element(locator, text)) is True

    def expect_to_be_enabled(self, locator):
        """Check if element is enabled."""
        logger.info("Checking if element with locator: %s is enabled", locator)
        assert self.wait.until(EC.element_to_be_clickable(locator)) is True

    def expect_to_be_disabled(self, locator):
        """Check if element is disabled."""
        logger.info("Checking if element with locator: %s is disabled", locator)
        assert self.wait.until(EC.element_to_be_clickable(locator)) is False

    def wait_for_element(self, locator):
        """Wait for element to be present on the page."""
        logger.info("Waiting for element with locator: %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator))

    def send_keys(self, locator, text):
        """Send keys to element."""
        if text is None:
            logger.info("Text is None, skipping send_keys for locator: %s", locator)
            return
        logger.info("Sending keys to element with locator: %s, text: %s", locator, text)
        self.wait_for_element(locator).send_keys(text)

    def get_text(self, locator):
        """Get text from element.

        Args:
            locator (tuple): Locator tuple containing By strategy and value

        Returns:
            str: Text content of the element if found
            str: Empty string if element not found or has no text
        """
        try:
            logger.info("Getting text from element with locator: %s", locator)
            element = self.wait_for_element(locator)
            text = element.text if element else ""
            logger.info("Got text: '%s'", text)
            return text
        except Exception as e:
            logger.warning("Failed to get text from element %s: %s", locator, str(e))
            return None
