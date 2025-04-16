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
        """Navigate to the specified URL."""
        self.driver.get(url)

    def wait_for_page_load(self):
        """Wait for page to load."""
        logger.debug("Waiting for page to load")

        # Method 1: Check if body tag is present
        self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        # Method 3: Check page readiness state
        def is_page_loaded(driver):
            return driver.execute_script("return document.readyState") == "complete"

        try:
            WebDriverWait(self.driver, 10).until(is_page_loaded)
            logger.info("Page DOM is fully loaded!")
        except TimeoutError:
            logger.error("Page DOM did not fully load")

        def are_ajax_requests_complete(driver):
            return driver.execute_script("return jQuery.active == 0")

        # Method 4: Check if all AJAX requests are complete
        try:
            WebDriverWait(self.driver, 10).until(are_ajax_requests_complete)
            logger.info("All AJAX requests completed!")
        except TimeoutError:
            logger.error("AJAX requests did not complete")

        # Method 5: Check if all images are loaded
        def are_images_loaded(driver):
            return driver.execute_script("return document.readyState") == "complete"

        try:
            WebDriverWait(self.driver, 10).until(are_images_loaded)
            logger.info("All images loaded!")
        except TimeoutError:
            logger.error("Images did not load")

        # Method 6: Check if all elements are present
        def are_elements_present(driver):
            return driver.execute_script("return document.readyState") == "complete"

        try:
            WebDriverWait(self.driver, 10).until(are_elements_present)
            logger.info("All elements present!")
        except TimeoutError:
            logger.error("Elements did not load")

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
        logger.debug("Clicking element with locator: %s", locator)
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
        logger.debug("Checking if element with locator: %s is visible", locator)
        element = self.wait.until(EC.visibility_of_element_located(locator))
        assert (
            element is not None
        ), f"Element with locator {locator} not found or not visible"

    def expect_to_have_text(self, locator, text):
        """Check if element has text."""
        logger.debug("Checking if element with locator: %s has text: %s", locator, text)
        assert self.wait.until(EC.text_to_be_present_in_element(locator, text)) is True

    def expect_to_be_enabled(self, locator):
        """Check if element is enabled."""
        logger.debug("Checking if element with locator: %s is enabled", locator)
        assert self.wait.until(EC.element_to_be_clickable(locator)) is True

    def expect_to_be_disabled(self, locator):
        """Check if element is disabled."""
        logger.debug("Checking if element with locator: %s is disabled", locator)
        assert self.wait.until(EC.element_to_be_clickable(locator)) is False

    def wait_for_element(self, locator):
        """Wait for element to be present on the page."""
        logger.debug("Waiting for element with locator: %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_timeout(self, timeout: float):
        """Wait for timeout using Selenium's built-in sleep."""
        logger.debug("Waiting for timeout: %s seconds", timeout)
        self.driver.implicitly_wait(timeout)

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
