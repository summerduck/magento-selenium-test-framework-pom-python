"""Module containing BasePage class for base page interactions."""

import logging
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

    def wait_for_element(self, locator):
        """Wait for element to be present on the page."""
        logger.debug("Waiting for element with locator: %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator))

    def click(self, locator):
        """Click on element."""
        logger.debug("Clicking element with locator: %s", locator)
        self.wait_for_element(locator).click()

    def send_keys(self, locator, text):
        """Send keys to element."""
        if text is None:
            logger.debug("Text is None, skipping send_keys for locator: %s", locator)
            return
        logger.debug(
            "Sending keys to element with locator: %s, text: %s", locator, text
        )
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
            logger.debug("Getting text from element with locator: %s", locator)
            element = self.wait_for_element(locator)
            text = element.text if element else ""
            logger.debug("Got text: '%s'", text)
            return text
        except Exception as e:
            logger.warning("Failed to get text from element %s: %s", locator, str(e))
            return None
