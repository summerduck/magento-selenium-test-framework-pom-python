"""Module containing SalePage class for sale page interactions."""

from dataclasses import dataclass
from typing import Dict, List
import logging
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

    def open_page(self) -> None:
        """Open and verify the sale page is loaded correctly."""
        logger.info("Navigating to Sale page at: %s", self.sale_page_url)
        self.goto(self.sale_page_url)
        self._verify_page_loaded()

    def _verify_page_loaded(self) -> None:
        """Verify the sale page is loaded correctly.

        Raises:
            TimeoutException: If page elements don't load within timeout
        """
        logger.info("Verifying Sale page elements and content are properly loaded")
        self.wait_for_page_load()
        self._verify_page_title()

    def _verify_page_title(self) -> None:
        """Verify the page title is correct.

        Raises:
            TimeoutException: If title element is not visible or doesn't match
        """
        logger.info("Verifying Sale page title")
        self.expect_to_be_visible(loc.PAGE_TITLE)
        self.expect_to_have_text(loc.PAGE_TITLE, "Sale")

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
            self.expect_to_be_visible(banner)

    def verify_promotional_content(self) -> None:
        """Verify promotional content text matches expected values.

        Raises:
            PromotionalContentError: If any promotional text doesn't match expected value
        """
        logger.info("Verifying promotional content")

        for locator, expected_text in self.promo_content.promo_mapping.items():
            try:
                actual_text = self.get_text(locator)
                if not actual_text or expected_text not in actual_text:
                    raise PromotionalContentError(
                        f"Expected text '{expected_text}' not found in '{actual_text}'"
                    )
                logger.info("Successfully verified promotional text: %s", expected_text)
            except Exception as e:
                logger.error(
                    "Failed to verify promotional text '%s': %s", expected_text, str(e)
                )
                raise PromotionalContentError(str(e)) from e

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
            self.expect_to_be_visible(section)
        logger.info("All deal sections titles are present on the page")

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

        # Verify at least one link is clickable from women's category
        if category_links["women's"]:
            self._verify_link_clickable(category_links["women's"][0])

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
        assert len(links) > 0, f"No {category_name} category links found"
        logger.info("Found %d %s category links", len(links), category_name)
        return links

    def _verify_link_clickable(self, link: WebElement) -> None:
        """Verify that a link element is clickable.

        Args:
            link: WebElement representing the link to verify

        Raises:
            AssertionError: If the link is not clickable
        """
        link_text = link.text
        logger.info("Verifying link '%s' is clickable", link_text)
        assert link.is_enabled(), f"Link '{link_text}' is not clickable"
