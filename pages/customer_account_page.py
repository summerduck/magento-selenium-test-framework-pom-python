"""Module containing CustomerAccountCreatePage class for account creation page interactions."""

import logging
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# Initialize logger
logger = logging.getLogger(__name__)


class CustomerAccountPage(BasePage):
    """Class for interacting with the customer account creation page."""

    page_url = "/customer/account/"

    # Success message locator
    SUCCESS_MESSAGE = (
        By.XPATH,
        "//div[contains(text(), 'Thank you for registering with Main Website Store.')]",
    )

    def __init__(
        self,
        driver,
    ):
        """
        Initialize the CustomerAccountCreatePage instance.
        """
        super().__init__(driver)
        self.customer_account_page_url = f"{self.base_url}{self.page_url}"

    def open_page(
        self,
    ):
        """
        Open the customer account creation page.
        """
        logger.info(
            "Navigating to Customer Account page at: %s", self.customer_account_page_url
        )
        self.goto(self.customer_account_page_url)

    def is_page_opened(
        self,
    ):
        """
        Check if the customer account creation page is opened
        """
        logger.info("Verifying Customer Account page is properly loaded")

        # Check if the current URL matches the expected URL
        assert self.driver.current_url == self.customer_account_page_url, (
            f"Expected URL: {self.customer_account_page_url}, "
            f"but got: {self.driver.current_url}"
        )
        logger.info(
            "✓ Confirmed: Current URL matches expected Customer Account page URL"
        )

        # Check if the customer account create page class is visible
        page_class = self.driver.find_element(
            "css selector", ".customer-account-create.page-layout-1column"
        )
        assert (
            page_class.is_displayed()
        ), "Customer Account page layout elements are not visible"
        logger.info("✓ Confirmed: Customer Account page layout is properly displayed")

    def verify_account_creation(
        self,
    ):
        """
        Verify account creation.
        """
        logger.info("Verifying successful customer account creation")
        self.wait_for_page_load()
        self.wait_for_element(self.SUCCESS_MESSAGE)
        self.expect_to_be_visible(self.SUCCESS_MESSAGE)
        logger.info("✓ Confirmed: Account creation success message is displayed")
