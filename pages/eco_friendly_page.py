"""Module containing EcoFriendlyPage class for eco-friendly page interactions."""

import logging
import time
from pages.base_page import BasePage
from pages.locators import EcoFriendlyPageLocators as loc

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

    def open_page(
        self,
    ):
        """
        Open the eco-friendly page.
        """
        # Open the page
        logger.info("Opening page: %s", self.eco_friendly_page_url)
        self.goto(self.eco_friendly_page_url)
        self.verify_page_loaded()

    def verify_page_loaded(self):
        """Verify the eco-friendly page is loaded correctly."""
        logger.info("Verifying eco-friendly page is loaded")
        self.wait_for_page_load()
        self.expect_to_be_visible(loc.PAGE_TITLE)
        self.expect_to_be_visible(loc.PRODUCT_GRID)
        time.sleep(0.5)

    def get_product_count(self):
        """Get the number of products displayed on the page."""
        logger.info("Getting product count")
        products = self.find_all(loc.PRODUCT_ITEMS_LIST)
        return len(products)

    # def sort_products(self, sort_by: str):
    #     """
    #     Sort products by the specified criteria.

    #     Args:
    #         sort_by (str): Sorting criteria (e.g., "position", "name", "price")
    #     """
    #     logger.info("Sorting products by: %s", sort_by)
    #     self.select_dropdown_option(loc.SORT_BY_DROPDOWN, sort_by)
    #     self.wait_for_page_load()

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
        self.verify_page_loaded()

    def set_products_per_page(self, count: str):
        """
        Set number of products to display per page.

        Args:
            count (str): Number of products per page (e.g., "12", "24", "36")
        """
        logger.info("Setting products per page to: %s", count)
        self.select_dropdown_option(loc.SHOW_PER_PAGE_DROPDOWN, count)
        self.wait_for_page_load()

    def get_product_prices(self):
        """Get list of product prices currently displayed."""
        logger.info("Getting product prices")
        return [element.text for element in self.find_all(loc.PRODUCT_PRICE)]

    def get_product_names(self):
        """Get list of product names currently displayed."""
        logger.info("Getting product names")
        sorted_names = [element.text for element in self.find_all(loc.PRODUCT_NAME)]
        self.sorted_names = sorted_names
        return sorted_names

    def verify_products_sorted_alphabetically(self):
        """Verify products are sorted alphabetically."""
        assert self.sorted_names == sorted(
            self.sorted_names
        ), "Products not sorted alphabetically"

    def count_products(self):
        """Count the number of products displayed on the page."""
        logger.info("Counting products")
        return len(self.find_all(loc.PRODUCT_NAME))
