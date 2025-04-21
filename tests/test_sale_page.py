"""Module containing tests for the sale page."""

from pytest import mark
import logging

logger = logging.getLogger(__name__)


class SalePageTest:
    """Test class for sale page functionality."""

    @mark.smoke
    def test_open_sale_page(
        self,
        sale_page,
    ):
        """
        Test basic sale page loading and verification title.
        """
        sale_page.open_page()

    @mark.ui_ux
    def test_promotional_banners(
        self,
        sale_page,
    ):
        """
        Test promotional banners are present and contain
        correct promotional information.
        """
        sale_page.open_page()
        sale_page.verify_promotional_banners()
        sale_page.verify_promotional_content()

    @mark.ui_ux
    def test_deal_sections(
        self,
        sale_page,
    ):
        """
        Test that all deal sections are present and
        contain the expected category links.
        """
        sale_page.open_page()
        sale_page.verify_deal_sections()
        sale_page.verify_category_links()
