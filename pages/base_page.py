"""Module containing BasePage class for base page interactions."""

from typing import Optional, List, Tuple
import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

# Initialize logger
logger = logging.getLogger(__name__)


class BasePage:
    """Base class for all page objects.

    This class provides common functionality for all page objects including:
    - Navigation methods
    - Element interaction methods
    - Wait conditions
    - Assertions
    - Element state checks
    """

    base_url: str = "https://magento.softwaretestingboard.com"
    page_url: Optional[str] = None
    DEFAULT_TIMEOUT: int = 10

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        """Initialize the base page.

        Args:
            driver: WebDriver instance
            timeout: Default timeout for wait operations in seconds
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    # Navigation methods
    def goto(self, url: str) -> None:
        """Navigate to the specified URL."""
        logger.debug("Navigating to URL: %s", url)
        self.driver.get(url)
        self.wait_for_page_load()

    def wait_for_page_load(self) -> None:
        """Wait for page to fully load by checking multiple conditions."""
        logger.debug("Waiting for page to load")

        try:
            # Wait for body tag
            self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            # Check document.readyState
            self.wait.until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )

            # Check jQuery.active if jQuery is present
            if self._is_jquery_present():
                self.wait.until(lambda d: d.execute_script("return jQuery.active == 0"))

            logger.info("Page loaded successfully")
        except TimeoutException as e:
            logger.error("Page load timeout: %s", str(e))
            raise

    def _is_jquery_present(self) -> bool:
        """Check if jQuery is present on the page."""
        return self.driver.execute_script("return typeof jQuery !== 'undefined'")

    def reload(self) -> "BasePage":
        """Reload the current page."""
        self.driver.refresh()
        self.wait_for_page_load()
        return self

    def back(self) -> "BasePage":
        """Navigate back in history."""
        self.driver.back()
        self.wait_for_page_load()
        return self

    def forward(self) -> "BasePage":
        """Navigate forward in history."""
        self.driver.forward()
        self.wait_for_page_load()
        return self

    @property
    def title(self) -> str:
        """Get page title."""
        return self.driver.title

    @property
    def current_url(self) -> str:
        """Get current URL."""
        return self.driver.current_url

    # Element interaction methods
    def click(self, locator: Tuple[By, str]) -> None:
        """Click on element.

        Args:
            locator: Tuple of By strategy and locator string
        """
        logger.debug("Clicking element with locator: %s", locator)
        self.wait_for_element(locator).click()

    def find(self, locator: Tuple[By, str]) -> WebElement:
        """Find an element on the page.

        Args:
            locator: Tuple of By strategy and locator string

        Returns:
            WebElement: Found element

        Raises:
            TimeoutException: If element is not found within timeout
        """
        return self.wait_for_element(locator)

    def find_all(self, locator: Tuple[By, str]) -> List[WebElement]:
        """Find all elements matching the locator.

        Args:
            locator: Tuple of By strategy and locator string

        Returns:
            List of WebElement objects
        """
        return self.driver.find_elements(*locator)

    # Wait methods
    def wait_for_element(self, locator: Tuple[By, str]) -> WebElement:
        """Wait for element to be present and return it.

        Args:
            locator: Tuple of By strategy and locator string

        Returns:
            WebElement: Found element

        Raises:
            TimeoutException: If element is not found within timeout
        """
        logger.debug("Waiting for element with locator: %s", locator)
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_for_timeout(self, timeout: float) -> None:
        """Explicit wait for specified time.

        Args:
            timeout: Time to wait in seconds
        """
        logger.debug("Waiting for %s seconds", timeout)
        self.driver.implicitly_wait(timeout)

    # Element interaction methods
    def send_keys(self, locator: Tuple[By, str], text: Optional[str]) -> None:
        """Send keys to element.

        Args:
            locator: Tuple of By strategy and locator string
            text: Text to send to element
        """
        if text is None:
            logger.debug("Text is None, skipping send_keys for locator: %s", locator)
            return

        logger.debug(
            "Sending keys to element with locator: %s, text: %s", locator, text
        )
        self.wait_for_element(locator).send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> Optional[str]:
        """Get text from element.

        Args:
            locator: Tuple of By strategy and locator string

        Returns:
            str: Text content of the element if found
            None: If element not found or has no text
        """
        try:
            logger.debug("Getting text from element with locator: %s", locator)
            element = self.wait_for_element(locator)
            text = element.text if element else ""
            logger.debug("Got text: '%s'", text)
            return text
        except WebDriverException as e:
            logger.warning("Failed to get text from element %s: %s", locator, str(e))
            return None

    # Assertion methods
    def expect_to_be_visible(self, locator: Tuple[By, str]) -> None:
        """Assert element is visible.

        Args:
            locator: Tuple of By strategy and locator string

        Raises:
            AssertionError: If element is not visible
        """
        logger.debug("Checking if element with locator: %s is visible", locator)
        element = self.wait.until(EC.visibility_of_element_located(locator))
        assert element is not None, (
            "Element with locator %s not found or not visible", locator
        )

    def expect_to_have_text(self, locator: Tuple[By, str], text: str) -> None:
        """Assert element has expected text.

        Args:
            locator: Tuple of By strategy and locator string
            text: Expected text

        Raises:
            AssertionError: If element does not have expected text
        """
        logger.debug("Checking if element with locator: %s has text: %s", locator, text)
        assert self.wait.until(EC.text_to_be_present_in_element(locator, text))

    def expect_to_be_enabled(self, locator: Tuple[By, str]) -> None:
        """Assert element is enabled.

        Args:
            locator: Tuple of By strategy and locator string

        Raises:
            AssertionError: If element is not enabled
        """
        logger.debug("Checking if element with locator: %s is enabled", locator)
        assert self.wait.until(EC.element_to_be_clickable(locator))

    def expect_to_be_disabled(self, locator: Tuple[By, str]) -> None:
        """Assert element is disabled.

        Args:
            locator: Tuple of By strategy and locator string

        Raises:
            AssertionError: If element is enabled
        """
        logger.debug("Checking if element with locator: %s is disabled", locator)
        assert not self.wait.until(EC.element_to_be_clickable(locator))
