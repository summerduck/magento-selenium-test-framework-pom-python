"""Module containing tests for the sale page."""

from pytest import mark
import logging
import time

logger = logging.getLogger(__name__)


class SalePageTest:
    """Test class for sale page functionality."""

    @mark.smoke
    def test_open_sale_page(
        self,
        sale_page,
    ):
        """Test basic sale page loading and verification."""
        sale_page.open_page()
        sale_page.verify_page_title()

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
