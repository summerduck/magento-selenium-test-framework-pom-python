"""Module containing SalePage class for sale page interactions."""

import logging
import time
from pages.base_page import BasePage
from pages.locators.locators import SalePageLocators as loc
from selenium.webdriver.common.by import By

# Initialize logger
logger = logging.getLogger(__name__)


class SalePage(BasePage):
    """Class for interacting with the sale page."""

    page_url = "/sale.html"

    def __init__(self, driver):
        """Initialize the SalePage instance."""
        super().__init__(driver)
        self.sale_page_url = f"{self.base_url}{self.page_url}"

    def open_page(self):
        """Open the sale page."""
        logger.info(
            "Navigating to Sale page at: %s",
            self.sale_page_url,
        )
        self.goto(self.sale_page_url)
        self._verify_page_loaded()

    def _verify_page_loaded(self):
        """Verify the sale page is loaded correctly."""
        logger.info("Verifying Sale page elements and content are properly loaded")
        self.wait_for_page_load()
        self.expect_to_be_visible(loc.PAGE_TITLE)
        self.expect_to_have_text(loc.PAGE_TITLE, "Sale")
        time.sleep(0.5)

    def verify_promotional_banners(self):
        """Verify promotional banners are present."""
        logger.info("Verifying promotional banners")
        self.expect_to_be_visible(loc.PROMO_BANNERS)
        time.sleep(3)
        self.expect_to_be_visible(loc.DISCOUNT_BANNER)
        self.expect_to_be_visible(loc.FREE_SHIPPING_BANNER)
        self.expect_to_be_visible(loc.TEES_PROMO)

    def verify_promotional_content(self):
        """Verify promotional content text."""
        logger.info("Verifying promotional content")

        # Dictionary of expected promotional texts
        promo_texts = {
            loc.DISCOUNT_BANNER: "20% OFF",
            loc.FREE_SHIPPING_BANNER: "Spend $50 or more — shipping is free!",
            loc.TEES_PROMO: "You can't have too many tees",
        }

        for locator, expected_text in promo_texts.items():
            try:
                actual_text = self.get_text(locator)
                assert (
                    expected_text in actual_text
                ), f"Expected text '{expected_text}' not found in '{actual_text}'"
                logger.info("Successfully verified promotional text: %s", expected_text)
            except Exception as e:
                logger.error(
                    "Failed to verify promotional text '%s': %s", expected_text, str(e)
                )
                raise

    def verify_deal_sections(self):
        """Verify all deal sections are present on the page."""
        logger.info("Verifying deal sections are present")

        # Check each deal section is visible
        self.expect_to_be_visible(loc.CATEGORIES_MENU)
        self.expect_to_be_visible(loc.WOMENS_DEALS_MENU_CATEGORY)
        self.expect_to_be_visible(loc.MENS_DEALS_MENU_CATEGORY)
        self.expect_to_be_visible(loc.GEAR_DEALS_MENU_CATEGORY)

        logger.info("All deal sections titles are present on the page")

    def verify_category_links(self):
        """Verify category links within each deal section."""
        logger.info("Verifying category links in each deal section")

        # Check women's category links
        womens_links = self.find_all(loc.WOMENS_CATEGORIES)
        assert len(womens_links) > 0, "No women's category links found"
        logger.info("Found %d women's category links", len(womens_links))

        # Check men's category links
        mens_links = self.find_all(loc.MENS_CATEGORIES)
        assert len(mens_links) > 0, "No men's category links found"
        logger.info("Found %d men's category links", len(mens_links))

        # Check gear category links
        gear_links = self.find_all(loc.GEAR_CATEGORIES)
        assert len(gear_links) > 0, "No gear category links found"
        logger.info("Found %d gear category links", len(gear_links))

        # Verify at least one link is clickable
        sample_link = womens_links[0]
        link_text = sample_link.text
        logger.info("Verifying link '%s' is clickable", link_text)
        assert sample_link.is_enabled(), f"Link '{link_text}' is not clickable"
