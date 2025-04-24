"""Module containing tests for the sale page."""

import logging
import allure
from pytest import mark

logger = logging.getLogger(__name__)


@allure.epic("E-commerce Platform")
@allure.feature("Sale Page")
class SalePageTest:
    """Test class for sale page functionality."""

    @allure.story("Basic Page Functionality")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Verify Sale page loads successfully")
    @allure.description(
        "Test verifies that the Sale page opens correctly and title is displayed"
    )
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

    @allure.story("Promotional Content")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify promotional banners display correctly")
    @allure.description(
        "Test verifies promotional banners are displayed and contain the expected content"
    )
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

    @allure.story("Deal Sections")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title("Verify deal sections and category links")
    @allure.description(
        "Test verifies all deal sections are present and category links are functional"
    )
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
