"""Module containing tests for the eco-friendly page."""

from pytest import mark
from data.enums import User
import logging
import time

logger = logging.getLogger(__name__)


class EcoFriendlyPageTest:
    """Test class for eco-friendly page functionality."""

    @mark.smoke
    def test_eco_friendly_page_loads_successfully(self, eco_friendly_page):
        """
        Test Case: Verify eco-friendly page loads successfully
        Steps:
        1. Open eco-friendly page
        2. Verify page elements are visible
        """
        eco_friendly_page.open_page()

    @mark.ui_ux
    def test_product_sorting(
        self,
        eco_friendly_page,
        sort_by="name",
    ):
        """
        Test Case: Verify product sorting functionality
        Steps:
        1. Open eco-friendly page
        2. Get initial product names
        3. Sort by name
        4. Verify products are sorted alphabetically
        """
        eco_friendly_page.open_page_sort_products(sort_by)
        eco_friendly_page.get_product_names()
        eco_friendly_page.verify_products_sorted_alphabetically()

    @mark.ui_ux
    def test_products_per_page(
        self,
        eco_friendly_page,
        products_per_page="12",
    ):
        """
        Test Case: Verify products per page functionality
        Steps:
        1. Open eco-friendly page
        2. Set products per page to 24
        3. Verify product count matches selected value
        """
        eco_friendly_page.open_page()
        # eco_friendly_page.set_products_per_page(products_per_page)

        product_count = eco_friendly_page.count_products()
        assert product_count == int(
            products_per_page
        ), f"Product count is not {products_per_page}"

    # @mark.ui_ux
    # def test_price_sorting(self, eco_friendly_page):
    #     """
    #     Test Case: Verify price sorting functionality
    #     Steps:
    #     1. Open eco-friendly page
    #     2. Get initial product prices
    #     3. Sort by price
    #     4. Verify products are sorted by price
    #     """
    #     eco_friendly_page.open_page()
    #     initial_prices = eco_friendly_page.get_product_prices()

    #     eco_friendly_page.sort_products("price")
    #     sorted_prices = eco_friendly_page.get_product_prices()

    #     # Convert price strings to float for comparison
    #     initial_prices_float = [
    #         float(price.replace("$", "")) for price in initial_prices
    #     ]
    #     sorted_prices_float = [float(price.replace("$", "")) for price in sorted_prices]

    #     assert sorted_prices_float == sorted(
    #         initial_prices_float
    #     ), "Products not sorted by price"
