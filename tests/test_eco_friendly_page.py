"""Module containing tests for the eco-friendly page."""

import logging
import allure
from pytest import mark

logger = logging.getLogger(__name__)


@allure.epic("E-commerce Platform")
@allure.feature("Eco-Friendly Page")
class EcoFriendlyPageTest:
    """Test class for eco-friendly page functionality."""

    @allure.story("Product Sorting")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify products can be sorted by {sort_by}")
    @allure.description(
        "Test verifies that products can be sorted by different criteria and validates the correct order"
    )
    @mark.parametrize("sort_by", ["name", "price", "position"])
    @mark.ui_ux
    def test_product_sorting(
        self,
        eco_friendly_page,
        sort_by: str,
    ):
        """
        Product Sorting Tests:
        - Verify products can be sorted by different criteria
        - Validate correct order of products after sorting

        Args:
            sort_by (str): The sorting criteria to test (name, price, or position)
        """
        eco_friendly_page.open_page_sort_products(sort_by)
        eco_friendly_page.get_product_names()
        eco_friendly_page.get_product_prices()
        eco_friendly_page.verify_products_sorted(sort_by)

    @allure.story("Products Per Page")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify {products_per_page} products per page display")
    @allure.description(
        "Test verifies that the correct number of products is displayed per page based on user selection"
    )
    @mark.parametrize("products_per_page", ["12", "24", "36"])
    @mark.ui_ux
    def test_show_products_per_page(
        self,
        eco_friendly_page,
        products_per_page: str,
    ):
        """
        Products Per Page Tests:
        - Verify number of products displayed matches selected option
        - Check product grid layout adjusts appropriately

        Args:
            products_per_page (str): Number of products to display per page (12, 24, or 36)
        """
        eco_friendly_page.open_page()
        eco_friendly_page.set_products_per_page(products_per_page)
        eco_friendly_page.count_products()
        eco_friendly_page.verify_products_per_page(products_per_page)

    @allure.story("Product View Modes")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify product view mode switching")
    @allure.description(
        "Test verifies that users can switch between grid and list view modes and product data remains consistent"
    )
    @mark.ui_ux
    def test_product_view_mode(
        self,
        eco_friendly_page,
    ):
        """
        Product View Mode Tests:
        - Verify default product grid view mode
        - Validate mode persistence after page refresh
        - Check product list view mode functionality
        - Ensure product data consistency between view modes
        - Verify smooth transitions between grid and list modes
        """
        # Verify default mode is product grid
        eco_friendly_page.open_page()
        eco_friendly_page.verify_product_grid_mode()

        # Check if the user's mode preference is preserved after page refresh
        eco_friendly_page.refresh_page()
        eco_friendly_page.verify_product_grid_mode()

        # Get product names list in default mode
        eco_friendly_page.get_product_names()

        # Switch to product list mode
        eco_friendly_page.switch_to_product_list_mode()
        eco_friendly_page.verify_product_list_mode()

        # Verify that product data remains consistent between mode switches
        eco_friendly_page.verify_product_data_consistency()

        # Switch back to product grid mode
        eco_friendly_page.switch_to_product_grid_mode()
        eco_friendly_page.verify_product_grid_mode()

        # Verify that product data remains consistent between mode switches
        eco_friendly_page.verify_product_data_consistency()
