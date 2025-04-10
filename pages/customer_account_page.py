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
        logger.info("Opening page: %s", self.customer_account_page_url)
        self.goto(self.customer_account_page_url)

    def is_page_opened(
        self,
    ):
        """
        Check if the customer account creation page is opened
        """
        logger.info("Checking if customer account creation page is opened")

        # Check if the current URL matches the expected URL
        assert self.driver.current_url == self.customer_account_page_url
        logger.info("Current URL matches expected URL")

        # Check if the customer account create page class is visible
        page_class = self.driver.find_element(
            "css selector", ".customer-account-create.page-layout-1column"
        )
        assert (
            page_class.is_displayed()
        ), "Customer account create page class is not visible"
        logger.info("Customer account create page class is visible")

    def verify_account_creation(
        self,
    ):
        """
        Verify account creation.
        """
        logger.info("Verifying account creation")
        self.wait_for_page_load()
        self.wait_for_element(self.SUCCESS_MESSAGE)
        self.expect_to_be_visible(self.SUCCESS_MESSAGE)
        logger.info("Account creation success message verified")
