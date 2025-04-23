"""Module containing tests for the sale page."""

import logging
from pytest import mark

logger = logging.getLogger(__name__)


class SalePageTest:
    """Test class for sale page functionality."""

    @mark.smoke
    def test_open_sale_page(
        self,
        sale_page,
    ):
        """
        Basic Page Load Test:
        - Verify sale page loads successfully
        - Validate page title is correct
        """
        sale_page.open_page()

    @mark.ui_ux
    def test_promotional_banners(
        self,
        sale_page,
    ):
        """
        Promotional Content Tests:
        - Verify promotional banners are displayed correctly
        - Validate promotional content matches expected information
        - Check banner visibility and placement
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
        Deal Sections Tests:
        - Verify all deal sections are present on the page
        - Validate category links within each deal section
        """
        sale_page.open_page()
        sale_page.verify_deal_sections()
        sale_page.verify_category_links()
