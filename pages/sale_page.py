"""Module containing SalePage class for sale page interactions."""

from dataclasses import dataclass
from typing import Dict, List
import logging
import allure
from selenium.webdriver.remote.webelement import WebElement
from pages.base_page import BasePage
from pages.locators.locators import SalePageLocators as loc

# Initialize logger
logger = logging.getLogger(__name__)


class SalePageException(Exception):
    """Base exception for SalePage-specific errors."""

    def __init__(self, message="An error occurred on the Sale Page"):
        self.message = message
        super().__init__(self.message)


class PromotionalContentError(SalePageException):
    """Raised when promotional content verification fails."""

    def __init__(self, message="Failed to verify promotional content"):
        super().__init__(message)


@dataclass
class PromotionalContent:
    """Structure for promotional content data."""

    discount_text: str = "20% OFF"
    free_shipping_text: str = "Spend $50 or more — shipping is free!"
    tees_promo_text: str = "You can't have too many tees"

    @property
    def promo_mapping(self) -> Dict:
        """Get mapping of locators to their expected text."""
        return {
            loc.DISCOUNT_BANNER: self.discount_text,
            loc.FREE_SHIPPING_BANNER: self.free_shipping_text,
            loc.TEES_PROMO: self.tees_promo_text,
        }


class SalePage(BasePage):
    """Class for interacting with the sale page.

    Attributes:
        page_url (str): The relative URL path for the sale page
        promo_content (PromotionalContent): Container for promotional text content
    """

    page_url: str = "/sale.html"
    promo_content: PromotionalContent = PromotionalContent()

    def __init__(self, driver) -> None:
        """Initialize the SalePage instance.

        Args:
            driver: WebDriver instance for browser control
        """
        super().__init__(driver)
        self.sale_page_url = f"{self.base_url}{self.page_url}"

    @allure.step("Opening the Sale page")
    def open_page(self) -> None:
        """Open and verify the sale page is loaded correctly."""
        logger.info("Navigating to Sale page at: %s", self.sale_page_url)
        self.goto(self.sale_page_url)
        self._verify_page_loaded()

    @allure.step("Verifying page is loaded correctly")
    def _verify_page_loaded(self) -> None:
        """Verify the sale page is loaded correctly.

        Raises:
            TimeoutException: If page elements don't load within timeout
        """
        logger.info("Verifying Sale page elements and content are properly loaded")
        self.wait_for_page_load()
        self._verify_page_title()

    @allure.step("Verifying page title")
    def _verify_page_title(self) -> None:
        """Verify the page title is correct.

        Raises:
            TimeoutException: If title element is not visible or doesn't match
        """
        logger.info("Verifying Sale page title")
        self.expect_to_be_visible(loc.PAGE_TITLE)
        self.expect_to_have_text(loc.PAGE_TITLE, "Sale")

    @allure.step("Verifying promotional banners are displayed")
    def verify_promotional_banners(self) -> None:
        """Verify all promotional banners are present and visible.

        Raises:
            TimeoutException: If any banner is not visible within timeout
        """
        logger.info("Verifying promotional banners")
        banners = [
            loc.PROMO_BANNERS,
            loc.DISCOUNT_BANNER,
            loc.FREE_SHIPPING_BANNER,
            loc.TEES_PROMO,
        ]
        for banner in banners:
            with allure.step(f"Checking banner visibility: {banner[1]}"):
                self.expect_to_be_visible(banner)

    @allure.step("Verifying promotional content text")
    def verify_promotional_content(self) -> None:
        """Verify promotional content text matches expected values.

        Raises:
            PromotionalContentError: If any promotional text doesn't match expected value
        """
        logger.info("Verifying promotional content")

        for locator, expected_text in self.promo_content.promo_mapping.items():
            try:
                with allure.step(
                    f"Verifying text '{expected_text}' in element {locator[1]}"
                ):
                    actual_text = self.get_text(locator)
                    allure.attach(
                        actual_text, "Actual Text", allure.attachment_type.TEXT
                    )
                    if not actual_text or expected_text not in actual_text:
                        raise PromotionalContentError(
                            f"Expected text '{expected_text}' not found in '{actual_text}'"
                        )
                    logger.info(
                        "Successfully verified promotional text: %s", expected_text
                    )
            except Exception as e:
                logger.error(
                    "Failed to verify promotional text '%s': %s", expected_text, str(e)
                )
                raise PromotionalContentError(str(e)) from e

    @allure.step("Verifying deal sections")
    def verify_deal_sections(self) -> None:
        """Verify all deal sections are present on the page.

        Raises:
            TimeoutException: If any deal section is not visible
        """
        logger.info("Verifying deal sections are present")
        sections = [
            loc.CATEGORIES_MENU,
            loc.WOMENS_DEALS_MENU_CATEGORY,
            loc.MENS_DEALS_MENU_CATEGORY,
            loc.GEAR_DEALS_MENU_CATEGORY,
        ]
        for section in sections:
            with allure.step(f"Checking section visibility: {section[1]}"):
                self.expect_to_be_visible(section)
        logger.info("All deal sections titles are present on the page")

    @allure.step("Verifying category links")
    def verify_category_links(self) -> None:
        """Verify category links within each deal section.

        Raises:
            AssertionError: If no links are found or if links are not clickable
        """
        logger.info("Verifying category links in each deal section")

        category_links = {
            "women's": self._get_category_links(loc.WOMENS_CATEGORIES),
            "men's": self._get_category_links(loc.MENS_CATEGORIES),
            "gear": self._get_category_links(loc.GEAR_CATEGORIES),
        }

        # Verify links are clickable for each category
        for category, links in category_links.items():
            if links:  # Check if list is not empty
                with allure.step(f"Verifying {category} category links are enabled"):
                    self._verify_link_enabled(links[0])

    @allure.step("Getting category links: {locator[1]}")
    def _get_category_links(self, locator: tuple) -> List[WebElement]:
        """Get category links and verify they exist.

        Args:
            locator: Tuple of By strategy and locator string

        Returns:
            List of WebElement objects representing category links

        Raises:
            AssertionError: If no links are found
        """
        links = self.find_all(locator)
        category_name = locator[1]  # Extract category name from locator

        with allure.step(f"Verifying {category_name} links exist"):
            assert len(links) > 0, f"No {category_name} category links found"
            allure.attach(
                str(len(links)),
                f"Number of {category_name} links",
                allure.attachment_type.TEXT,
            )
            logger.info("Found %d %s category links", len(links), category_name)

        return links

    @allure.step("Verifying link is enabled")
    def _verify_link_enabled(self, link: WebElement) -> None:
        """Verify that a link element is enabled.

        Args:
            link: WebElement representing the link to verify

        Raises:
            AssertionError: If the link is not enabled
        """
        logger.info("Verifying link is enabled")
        assert link.is_displayed() and link.is_enabled(), "Link is not enabled"
