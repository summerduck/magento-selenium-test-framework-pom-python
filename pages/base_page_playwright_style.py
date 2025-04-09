from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import logging
import time


class BasePage:
    """
    BasePage class that provides Playwright-like methods for Selenium WebDriver.
    """

    def __init__(self, driver, base_url=None, timeout=10):
        """
        Initialize the BasePage with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
            base_url: Base URL for the application
            timeout: Default timeout for waits in seconds
        """
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.logger = logging.getLogger(__name__)

    # Navigation methods

    def goto(self, url):
        """Navigate to URL (relative or absolute)"""
        if url.startswith("http"):
            self.driver.get(url)
        elif self.base_url:
            self.driver.get(f"{self.base_url.rstrip('/')}/{url.lstrip('/')}")
        else:
            raise ValueError("Base URL is not set and relative URL was provided")
        return self

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

    # Locator methods

    def locator(self, selector, selector_type=None):
        """
        Create a locator object for further operations.
        Example: page.locator("#submit-button").click()
        """
        return Locator(self.driver, selector, selector_type, self.timeout)

    # Actions

    def click(self, selector, selector_type=None, timeout=None):
        """Click on element"""
        timeout = timeout or self.timeout
        return self.locator(selector, selector_type).click(timeout=timeout)

    def fill(self, selector, value, selector_type=None, timeout=None):
        """Clear and fill input field"""
        timeout = timeout or self.timeout
        return self.locator(selector, selector_type).fill(value, timeout=timeout)

    def type(self, selector, text, delay=0, selector_type=None):
        """Type text with optional delay between keystrokes"""
        return self.locator(selector, selector_type).type(text, delay)

    def select_option(
        self, selector, value=None, label=None, index=None, selector_type=None
    ):
        """Select option from dropdown"""
        return self.locator(selector, selector_type).select_option(value, label, index)

    def check(self, selector, selector_type=None):
        """Check a checkbox"""
        return self.locator(selector, selector_type).check()

    def uncheck(self, selector, selector_type=None):
        """Uncheck a checkbox"""
        return self.locator(selector, selector_type).uncheck()

    def hover(self, selector, selector_type=None):
        """Hover over element"""
        return self.locator(selector, selector_type).hover()

    def drag_to(self, source, target, source_type=None, target_type=None):
        """Drag source element to target element"""
        source_elem = self.locator(source, source_type).element()
        target_elem = self.locator(target, target_type).element()

        actions = ActionChains(self.driver)
        actions.drag_and_drop(source_elem, target_elem).perform()
        return self

    def press(self, selector, key, selector_type=None):
        """Press keyboard key on element"""
        return self.locator(selector, selector_type).press(key)

    # Getters

    def text_content(self, selector, selector_type=None):
        """Get text content of element"""
        return self.locator(selector, selector_type).text_content()

    def get_attribute(self, selector, attr, selector_type=None):
        """Get attribute of element"""
        return self.locator(selector, selector_type).get_attribute(attr)

    def is_visible(self, selector, selector_type=None, timeout=None):
        """Check if element is visible"""
        timeout = timeout or self.timeout
        return self.locator(selector, selector_type).is_visible(timeout)

    def is_hidden(self, selector, selector_type=None, timeout=None):
        """Check if element is hidden"""
        timeout = timeout or self.timeout
        return not self.is_visible(selector, selector_type, timeout)

    def is_enabled(self, selector, selector_type=None):
        """Check if element is enabled"""
        return self.locator(selector, selector_type).is_enabled()

    def is_disabled(self, selector, selector_type=None):
        """Check if element is disabled"""
        return not self.is_enabled(selector, selector_type)

    def is_checked(self, selector, selector_type=None):
        """Check if checkbox is checked"""
        return self.locator(selector, selector_type).is_checked()

    # Waits

    def wait_for_selector(
        self, selector, state="visible", timeout=None, selector_type=None
    ):
        """
        Wait for selector to reach state.

        Args:
            selector: Element selector
            state: State to wait for ('visible', 'hidden', 'attached', 'detached')
            timeout: Timeout in seconds
            selector_type: Selector type if not CSS
        """
        timeout = timeout or self.timeout
        return self.locator(selector, selector_type).wait_for(state, timeout)

    def wait_for_navigation(self, timeout=None):
        """Wait for navigation to complete"""
        timeout = timeout or self.timeout
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            self.logger.warning("Navigation did not complete in %s seconds", timeout)
            return False

    def wait_for_load_state(self, state="load", timeout=None):
        """
        Wait for page load state.

        Args:
            state: State to wait for ('load', 'domcontentloaded', 'networkidle')
            timeout: Timeout in seconds
        """
        timeout = timeout or self.timeout
        if state == "load":
            return self.wait_for_navigation(timeout)
        elif state == "domcontentloaded":
            try:
                WebDriverWait(self.driver, timeout).until(
                    lambda d: d.execute_script("return document.readyState")
                    != "loading"
                )
                return True
            except TimeoutException:
                return False
        elif state == "networkidle":
            # This is approximated in Selenium
            time.sleep(0.5)  # Short delay to let network requests start
            try:
                # Wait a bit and check if document is complete
                WebDriverWait(self.driver, timeout).until(
                    lambda d: d.execute_script("return document.readyState")
                    == "complete"
                )
                time.sleep(0.5)  # Additional delay to ensure network is idle
                return True
            except TimeoutException:
                return False
        else:
            raise ValueError("Unknown load state: %s" % state)

    # JavaScript execution

    def evaluate(self, script, *args):
        """Evaluate JavaScript in the page"""
        return self.driver.execute_script(script, *args)

    # Screenshots and debugging

    def screenshot(self, path=None):
        """Take screenshot of the page"""
        if path:
            return self.driver.save_screenshot(path)
        else:
            return self.driver.get_screenshot_as_base64()

    def element_screenshot(self, selector, path, selector_type=None):
        """Take screenshot of specific element"""
        element = self.locator(selector, selector_type).element()
        self.evaluate("arguments[0].scrollIntoView()", element)
        return element.screenshot(path)


class Locator:
    """
    Locator class for handling element selectors in a Playwright-style way.
    """

    def __init__(self, driver, selector, selector_type=None, timeout=10):
        """
        Initialize Locator with WebDriver and selector.

        Args:
            driver: Selenium WebDriver instance
            selector: Element selector
            selector_type: Type of selector (css, xpath, id, class, name, tag, link_text)
            timeout: Default timeout for waits
        """
        self.driver = driver
        self.selector = selector
        self.selector_type = selector_type
        self.timeout = timeout

        # Map selector_type to Selenium By
        from selenium.webdriver.common.by import By

        self.by_mapping = {
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "id": By.ID,
            "class": By.CLASS_NAME,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT,
        }

        # Infer selector type if not provided
        if not selector_type:
            if selector.startswith("//") or selector.startswith("(//"):
                self.by = By.XPATH
            elif selector.startswith("#"):
                self.by = By.CSS_SELECTOR
            else:
                self.by = By.CSS_SELECTOR
        else:
            self.by = self.by_mapping.get(selector_type.lower(), By.CSS_SELECTOR)

    def element(self, timeout=None):
        """Get the element with wait"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(
            self.driver, timeout, ignored_exceptions=[StaleElementReferenceException]
        )
        return wait.until(EC.presence_of_element_located((self.by, self.selector)))

    def elements(self, timeout=None):
        """Get all matching elements with wait"""
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_all_elements_located((self.by, self.selector)))

    def click(self, force=False, timeout=None):
        """Click the element"""
        timeout = timeout or self.timeout
        try:
            if force:
                # Force click via JavaScript
                element = self.element(timeout)
                self.driver.execute_script("arguments[0].click();", element)
            else:
                wait = WebDriverWait(self.driver, timeout)
                element = wait.until(
                    EC.element_to_be_clickable((self.by, self.selector))
                )
                element.click()
            return self
        except Exception as e:
            logging.error("Failed to click element: %s", str(e))
            raise

    def fill(self, value, timeout=None):
        """Clear and fill input field"""
        timeout = timeout or self.timeout
        element = self.element(timeout)
        element.clear()
        element.send_keys(value)
        return self

    def type(self, text, delay=0):
        """Type text with optional delay between keystrokes"""
        element = self.element()
        element.clear()
        for char in text:
            element.send_keys(char)
            if delay > 0:
                time.sleep(delay)
        return self

    def select_option(self, value=None, label=None, index=None):
        """Select option from dropdown"""
        from selenium.webdriver.support.ui import Select

        select = Select(self.element())

        if value is not None:
            select.select_by_value(value)
        elif label is not None:
            select.select_by_visible_text(label)
        elif index is not None:
            select.select_by_index(index)
        else:
            raise ValueError("Must provide value, label, or index")

        return self

    def check(self):
        """Check a checkbox"""
        element = self.element()
        if not element.is_selected():
            element.click()
        return self

    def uncheck(self):
        """Uncheck a checkbox"""
        element = self.element()
        if element.is_selected():
            element.click()
        return self

    def hover(self):
        """Hover over element"""
        element = self.element()
        ActionChains(self.driver).move_to_element(element).perform()
        return self

    def press(self, key):
        """Press keyboard key on element"""
        key_mapping = {
            "Enter": Keys.ENTER,
            "Tab": Keys.TAB,
            "Escape": Keys.ESCAPE,
            "Backspace": Keys.BACK_SPACE,
            "Delete": Keys.DELETE,
            "ArrowUp": Keys.ARROW_UP,
            "ArrowDown": Keys.ARROW_DOWN,
            "ArrowLeft": Keys.ARROW_LEFT,
            "ArrowRight": Keys.ARROW_RIGHT,
            "Home": Keys.HOME,
            "End": Keys.END,
            "PageUp": Keys.PAGE_UP,
            "PageDown": Keys.PAGE_DOWN,
        }

        element = self.element()
        if key in key_mapping:
            element.send_keys(key_mapping[key])
        else:
            # Single character key
            element.send_keys(key)
        return self

    def text_content(self):
        """Get text content of element"""
        return self.element().text

    def get_attribute(self, attr):
        """Get attribute of element"""
        return self.element().get_attribute(attr)

    def wait_for(self, state="visible", timeout=None):
        """
        Wait for element to reach state.

        Args:
            state: State to wait for ('visible', 'hidden', 'attached', 'detached')
            timeout: Timeout in seconds
        """
        timeout = timeout or self.timeout
        wait = WebDriverWait(self.driver, timeout)

        try:
            if state == "visible":
                wait.until(EC.visibility_of_element_located((self.by, self.selector)))
            elif state == "hidden":
                wait.until(EC.invisibility_of_element_located((self.by, self.selector)))
            elif state == "attached":
                wait.until(EC.presence_of_element_located((self.by, self.selector)))
            elif state == "detached":
                wait.until_not(EC.presence_of_element_located((self.by, self.selector)))
            else:
                raise ValueError("Unknown state: %s" % state)
            return True
        except TimeoutException:
            return False

    def is_visible(self, timeout=0):
        """Check if element is visible"""
        if timeout > 0:
            return self.wait_for("visible", timeout)
        try:
            element = self.driver.find_element(self.by, self.selector)
            return element.is_displayed()
        except:
            return False

    def is_enabled(self):
        """Check if element is enabled"""
        try:
            return self.element().is_enabled()
        except:
            return False

    def is_checked(self):
        """Check if checkbox is checked"""
        try:
            return self.element().is_selected()
        except:
            return False
