"""Module containing tests for the eco-friendly page."""

from pytest import mark
import logging

logger = logging.getLogger(__name__)


class EcoFriendlyPageTest:
    """Test class for eco-friendly page functionality."""

    @mark.parametrize("sort_by", ["name", "price", "position"])
    @mark.ui_ux
    def test_product_sorting(
        self,
        eco_friendly_page,
        sort_by,
    ):
        """
        Verify product sorting functionality
        """
        eco_friendly_page.open_page_sort_products(sort_by)
        eco_friendly_page.get_product_names()
        eco_friendly_page.get_product_prices()
        eco_friendly_page.verify_products_sorted(sort_by)

    @mark.parametrize("products_per_page", ["12", "24", "36"])
    @mark.ui_ux
    def test_show_products_per_page(
        self,
        eco_friendly_page,
        products_per_page,
    ):
        """
        Verify show products per page functionality
        """
        eco_friendly_page.open_page()
        eco_friendly_page.set_products_per_page(products_per_page)
        eco_friendly_page.count_products()
        eco_friendly_page.verify_products_per_page(products_per_page)

    def test_product_view_mode(
        self,
        eco_friendly_page,
    ):
        """
        Verify mode switch functionality
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
