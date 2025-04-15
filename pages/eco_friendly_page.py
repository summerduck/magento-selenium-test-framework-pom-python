"""Module containing EcoFriendlyPage class for eco-friendly page interactions."""

import logging
import time
from pages.base_page import BasePage
from pages.locators import EcoFriendlyPageLocators as loc
from selenium.webdriver.common.by import By

# Initialize logger
logger = logging.getLogger(__name__)


class EcoFriendlyPage(BasePage):
    """Class for interacting with the eco-friendly page."""

    page_url = "/collections/eco-friendly.html"

    def __init__(
        self,
        driver,
    ):
        """
        Initialize the EcoFriendlyPage instance.
        """
        super().__init__(driver)
        self.eco_friendly_page_url = f"{self.base_url}{self.page_url}"
        self.sorted_names = []
        self.sorted_prices = []
        self.products_per_page = None

    def open_page(
        self,
    ):
        """
        Open the eco-friendly page.
        """
        # Open the page
        logger.info("Opening page: %s", self.eco_friendly_page_url)
        self.goto(self.eco_friendly_page_url)
        self._verify_page_loaded()

    def refresh_page(self):
        """Refresh the page."""
        logger.info("Refreshing page")
        self.driver.refresh()
        self._verify_page_loaded()

    def _verify_page_loaded(self):
        """Verify the eco-friendly page is loaded correctly."""
        logger.info("Verifying eco-friendly page is loaded")
        self.wait_for_page_load()
        self.expect_to_be_visible(loc.PAGE_TITLE)
        time.sleep(0.5)

    def open_page_sort_products(self, sort_by: str):
        """
        Open page and sort products by the specified criteria.

        Args:
            sort_by (str): Sorting criteria ('position', 'name', or 'price')
        """
        logger.info("Opening page and sorting products by: %s", sort_by)

        sort_urls = {
            "position": self.eco_friendly_page_url,
            "name": f"{self.eco_friendly_page_url}?product_list_order=name",
            "price": f"{self.eco_friendly_page_url}?product_list_order=price",
        }

        if sort_by not in sort_urls:
            raise ValueError(
                f"Invalid sort_by value: {sort_by}. Must be one of: {list(sort_urls.keys())}"
            )

        self.goto(sort_urls[sort_by])
        self._verify_page_loaded()

    def set_products_per_page(self, count: str):
        """
        Set number of products to display per page.

        Args:
            count (str): Number of products per page (e.g., "12", "24", "36")
        """
        logger.info("Setting products per page to: %s", count)
        self.wait_for_element(loc.SHOW_PER_PAGE_DROPDOWN).click()
        self.wait_for_element(
            (By.XPATH, f"(//select[@id='limiter'])[2]//option[@value='{count}']")
        ).click()
        self.wait_for_page_load()

    def get_product_names(self):
        """Get list of product names currently displayed."""
        logger.info("Getting product names")
        self.sorted_names = [
            element.text for element in self.find_all(loc.PRODUCT_NAME)
        ]
        logger.info("Product names: %s", self.sorted_names)
        return self.sorted_names

    def get_product_prices(self):
        """Get list of product prices currently displayed."""
        logger.info("Getting product prices")
        self.sorted_prices = [
            element.text for element in self.find_all(loc.PRODUCT_PRICE)
        ]
        return self.sorted_prices

    def verify_products_sorted_alphabetically(self):
        """Verify products are sorted alphabetically."""
        logger.info("Verifying products are sorted alphabetically")
        logger.info("Sorted names: %s", self.sorted_names)
        assert self.sorted_names == sorted(
            self.sorted_names
        ), "Products not sorted alphabetically"
        logger.info("Products sorted alphabetically")

    def verify_products_sorted_by_price(self):
        """Verify products are sorted by price."""
        logger.info("Verifying products are sorted by price")
        logger.info("Sorted prices: %s", self.sorted_prices)
        assert self.sorted_prices == sorted(
            self.sorted_prices
        ), "Products not sorted by price"
        logger.info("Products sorted by price")

    def verify_products_sorted_by_position(self):
        """Verify products are sorted by position."""
        logger.info("Verifying products are sorted by position")
        logger.info("Sorted prices: %s", self.sorted_prices)
        assert self.sorted_prices != sorted(
            self.sorted_prices
        ), "Products not sorted by price"
        logger.info("Sorted names: %s", self.sorted_names)
        assert self.sorted_names != sorted(
            self.sorted_names
        ), "Products not sorted alphabetically"
        logger.info("Products sorted by position")

    def verify_products_sorted(self, sort_by: str):
        """Verify products are sorted by the specified criteria."""
        if sort_by == "name":
            self.verify_products_sorted_alphabetically()
        elif sort_by == "price":
            self.verify_products_sorted_by_price()
        elif sort_by == "position":
            self.verify_products_sorted_by_position()

    def count_products(self):
        """Count the number of products displayed on the page."""
        logger.info("Counting products")
        time.sleep(1)
        self.products_per_page = len(self.find_all(loc.PRODUCT_ITEM))
        logger.info("Products per page: %s", self.products_per_page)

        return self.products_per_page

    def verify_products_per_page(self, count: str):
        """Verify the number of products per page."""
        logger.info("Verifying products per page")

        # Get max number of products
        total_products_count = self.get_total_products_count()

        # Verify the number of products per page
        if total_products_count < int(count):
            assert self.products_per_page == total_products_count, (
                "Products per page is not %s",
                total_products_count,
            )
        else:
            assert self.products_per_page == int(count), (
                "Products per page is not %s, it is %s",
                count,
                self.products_per_page,
            )
        logger.info("Products per page verified")

    def get_total_products_count(self):
        """
        Get the total number of products in the category.

        Returns:
            int: Total number of products
        """
        logger.info("Getting total products count")
        total_count = self.get_text(loc.TOTAL_PRODUCTS_COUNT)
        logger.info("Total products count: %s", total_count)
        return int(total_count)

    def verify_product_grid_mode(self):
        """Verify product grid mode."""
        logger.info("Verifying product grid mode")
        self.expect_to_be_visible(loc.ACTIVE_GRID_MODE)
        self.expect_to_be_visible(loc.PRODUCT_GRID)
        logger.info("Product grid mode verified")

    def verify_product_list_mode(self):
        """Verify product list mode."""
        logger.info("Verifying product list mode")
        self.expect_to_be_visible(loc.ACTIVE_LIST_MODE)
        self.expect_to_be_visible(loc.PRODUCT_LIST)
        assert (
            self.driver.current_url
            == self.eco_friendly_page_url + "?product_list_mode=list"
        )
        logger.info("Product list mode verified")

    def switch_to_product_grid_mode(self):
        """Switch to product grid mode."""
        logger.info("Switching to product grid mode")
        self.click(loc.GRID_MODE)
        self._verify_page_loaded()
        logger.info("Switched to product grid mode")

    def switch_to_product_list_mode(self):
        """Switch to product list mode."""
        logger.info("Switching to product list mode")
        self.click(loc.LIST_MODE)
        self._verify_page_loaded()
        logger.info("Switched to product list mode")

    def verify_product_data_consistency(self):
        """Verify that product data remains consistent between mode switches."""
        product_names_list_mode = self.get_product_names()
        assert all(
            name in self.sorted_names for name in product_names_list_mode
        ), "Product names are not consistent between mode switches"
        logger.info("Product data consistency verified")
