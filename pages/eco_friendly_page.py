"""Module containing EcoFriendlyPage class for eco-friendly page interactions."""

import logging
import time
import allure
from selenium.webdriver.common.by import By
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
        self.sorted_prices = []
        self.products_per_page = None

    @allure.step("Opening the Eco-Friendly page")
    def open_page(
        self,
    ):
        """
        Open the eco-friendly page.
        """
        logger.info(
            "Navigating to Eco-Friendly Products page at: %s",
            self.eco_friendly_page_url,
        )
        self.goto(self.eco_friendly_page_url)
        self._verify_page_loaded()

    @allure.step("Refreshing the Eco-Friendly page")
    def refresh_page(self):
        """Refresh the page."""
        logger.info("Refreshing Eco-Friendly Products page")
        self.driver.refresh()
        self._verify_page_loaded()

    @allure.step("Verifying page is loaded correctly")
    def _verify_page_loaded(self):
        """Verify the eco-friendly page is loaded correctly."""
        logger.info(
            "Verifying Eco-Friendly page elements and content are properly loaded"
        )
        self.wait_for_page_load()
        self.expect_to_be_visible(loc.PAGE_TITLE)
        time.sleep(0.5)

    @allure.step("Opening page and sorting products by: {sort_by}")
    def open_page_sort_products(self, sort_by: str):
        """
        Open page and sort products by the specified criteria.

        Args:
            sort_by (str): Sorting criteria ('position', 'name', or 'price')
        """
        logger.info(
            "Opening Eco-Friendly page and applying sorting filter: '%s'", sort_by
        )

        sort_urls = {
            "position": self.eco_friendly_page_url,
            "name": f"{self.eco_friendly_page_url}?product_list_order=name",
            "price": f"{self.eco_friendly_page_url}?product_list_order=price",
        }

        if sort_by not in sort_urls:
            logger.error(
                "Invalid sorting option '%s'. Valid options are: %s",
                sort_by,
                list(sort_urls.keys()),
            )
            raise ValueError(
                f"Invalid sort_by value: {sort_by}. Must be one of: {list(sort_urls.keys())}"
            )

        self.goto(sort_urls[sort_by])
        self._verify_page_loaded()

    @allure.step("Setting products per page to: {count}")
    def set_products_per_page(self, count: str):
        """
        Set number of products to display per page.

        Args:
            count (str): Number of products per page (e.g., "12", "24", "36")
        """
        logger.info("Changing products display limit to %s items per page", count)
        with allure.step("Clicking on 'Show per page' dropdown"):
            self.wait_for_element(loc.SHOW_PER_PAGE_DROPDOWN).click()

        with allure.step(f"Selecting option: {count} products per page"):
            self.wait_for_element(
                (By.XPATH, f"(//select[@id='limiter'])[2]//option[@value='{count}']")
            ).click()

        self.wait_for_page_load()

    @allure.step("Getting product names")
    def get_product_names(self):
        """Get list of product names currently displayed."""
        logger.info("Retrieving names of all displayed products on the current page")
        self.sorted_names = [
            element.text for element in self.find_all(loc.PRODUCT_NAME)
        ]

        allure.attach(
            "\n".join(self.sorted_names), "Product Names", allure.attachment_type.TEXT
        )

        logger.info("Found %d products: %s", len(self.sorted_names), self.sorted_names)
        return self.sorted_names

    @allure.step("Getting product prices")
    def get_product_prices(self):
        """Get list of product prices currently displayed."""
        logger.info("Retrieving prices of all displayed products on the current page")
        self.sorted_prices = [
            element.text for element in self.find_all(loc.PRODUCT_PRICE)
        ]

        allure.attach(
            "\n".join(self.sorted_prices), "Product Prices", allure.attachment_type.TEXT
        )

        logger.info("Found %d prices: %s", len(self.sorted_prices), self.sorted_prices)
        return self.sorted_prices

    @allure.step("Verifying products are sorted alphabetically")
    def verify_products_sorted_alphabetically(self):
        """Verify products are sorted alphabetically."""
        logger.info("Verifying products are correctly sorted in alphabetical order")
        logger.info("Current product order: %s", self.sorted_names)

        sorted_names = sorted(self.sorted_names)
        is_sorted = self.sorted_names == sorted_names

        allure.attach(
            f"Current order: {self.sorted_names}\nExpected order: {sorted_names}",
            "Alphabetical Sort Comparison",
            allure.attachment_type.TEXT,
        )

        assert is_sorted, "Products are not in alphabetical order"
        logger.info("✓ Confirmed: Products are correctly sorted alphabetically")

    @allure.step("Verifying products are sorted by price")
    def verify_products_sorted_by_price(self):
        """Verify products are sorted by price."""
        logger.info("Verifying products are correctly sorted by price (ascending)")
        logger.info("Current price order: %s", self.sorted_prices)

        sorted_prices = sorted(self.sorted_prices)
        is_sorted = self.sorted_prices == sorted_prices

        allure.attach(
            f"Current order: {self.sorted_prices}\nExpected order: {sorted_prices}",
            "Price Sort Comparison",
            allure.attachment_type.TEXT,
        )

        assert is_sorted, "Products are not sorted by price correctly"
        logger.info("✓ Confirmed: Products are correctly sorted by price")

    @allure.step("Verifying products are sorted by position")
    def verify_products_sorted_by_position(self):
        """Verify products are sorted by position."""
        logger.info("Verifying products are in default position order")

        price_sorted = self.sorted_prices == sorted(self.sorted_prices)
        name_sorted = self.sorted_names == sorted(self.sorted_names)

        allure.attach(
            f"Is price sorted: {price_sorted}\nIs name sorted: {name_sorted}",
            "Position Sort Check",
            allure.attachment_type.TEXT,
        )

        assert not price_sorted, "Products appear to be sorted by price"
        assert not name_sorted, "Products appear to be sorted alphabetically"
        logger.info("✓ Confirmed: Products are in default position order")

    @allure.step("Verifying products are sorted by: {sort_by}")
    def verify_products_sorted(self, sort_by: str):
        """Verify products are sorted by the specified criteria."""
        if sort_by == "name":
            self.verify_products_sorted_alphabetically()
        elif sort_by == "price":
            self.verify_products_sorted_by_price()
        elif sort_by == "position":
            self.verify_products_sorted_by_position()

    @allure.step("Counting products on page")
    def count_products(self):
        """Count the number of products displayed on the page."""
        logger.info("Counting total number of products displayed on current page")
        time.sleep(1)
        self.products_per_page = len(self.find_all(loc.PRODUCT_ITEM))

        allure.attach(
            str(self.products_per_page), "Products Count", allure.attachment_type.TEXT
        )

        logger.info("Found %d products on current page", self.products_per_page)
        return self.products_per_page

    @allure.step("Verifying products per page: {count}")
    def verify_products_per_page(self, count: str):
        """Verify the number of products per page."""
        logger.info(
            "Verifying correct number of products (%s) are displayed per page", count
        )

        # Get max number of products
        total_products_count = self.get_total_products_count()

        # Verify the number of products per page
        if total_products_count < int(count):
            logger.info(
                "Total products (%d) is less than requested per page (%s)",
                total_products_count,
                count,
            )
            assert (
                self.products_per_page == total_products_count
            ), f"Expected {total_products_count} products, but found {self.products_per_page}"
        else:
            assert self.products_per_page == int(
                count
            ), f"Expected {count} products per page, but found {self.products_per_page}"
        logger.info("✓ Confirmed: Correct number of products displayed per page")

    @allure.step("Getting total products count")
    def get_total_products_count(self):
        """
        Get the total number of products in the category.

        Returns:
            int: Total number of products
        """
        logger.info("Retrieving total number of products in Eco-Friendly category")
        total_count = self.get_text(loc.TOTAL_PRODUCTS_COUNT)

        allure.attach(total_count, "Total Products Count", allure.attachment_type.TEXT)

        logger.info("Total products in category: %s", total_count)
        return int(total_count)

    @allure.step("Verifying product grid mode")
    def verify_product_grid_mode(self):
        """Verify product grid mode."""
        logger.info("Verifying products are displayed in grid view mode")
        self.expect_to_be_visible(loc.ACTIVE_GRID_MODE)
        self.expect_to_be_visible(loc.PRODUCT_GRID)
        logger.info("✓ Confirmed: Products are displayed in grid view")

    @allure.step("Verifying product list mode")
    def verify_product_list_mode(self):
        """Verify product list mode."""
        logger.info("Verifying products are displayed in list view mode")
        self.expect_to_be_visible(loc.ACTIVE_LIST_MODE)
        self.expect_to_be_visible(loc.PRODUCT_LIST)
        assert (
            self.driver.current_url
            == self.eco_friendly_page_url + "?product_list_mode=list"
        )
        logger.info("✓ Confirmed: Products are displayed in list view")

    @allure.step("Switching to product grid mode")
    def switch_to_product_grid_mode(self):
        """Switch to product grid mode."""
        logger.info("Switching product display to grid view mode")
        self.click(loc.GRID_MODE)
        self._verify_page_loaded()

    @allure.step("Switching to product list mode")
    def switch_to_product_list_mode(self):
        """Switch to product list mode."""
        logger.info("Switching product display to list view mode")
        self.click(loc.LIST_MODE)
        self._verify_page_loaded()

    @allure.step("Verifying product data consistency")
    def verify_product_data_consistency(self):
        """Verify that product data remains consistent between mode switches."""
        logger.info("Verifying product data consistency across view mode changes")
        product_names_list_mode = self.get_product_names()

        # Comparing product lists
        is_consistent = all(
            name in self.sorted_names for name in product_names_list_mode
        )

        allure.attach(
            f"Original list: {self.sorted_names}\nNew list: {product_names_list_mode}\nConsistent: {is_consistent}",
            "Product Data Comparison",
            allure.attachment_type.TEXT,
        )

        assert is_consistent, "Product data mismatch detected between view modes"
        logger.info(
            "✓ Confirmed: Product data remains consistent across view mode changes"
        )
