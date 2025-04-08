"""Pytest configuration file for Selenium tests with fixture definitions."""

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pytest
from pages.customer_account_create_page import CustomerAccountCreatePage
from pages.eco_friendly_page import EcoFriendlyPage
from pages.sale_page import SalePage


@pytest.fixture()
def driver():
    """Fixture to initialize the Chrome driver with necessary options."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    chrome_driver = webdriver.Chrome(options=options)
    return chrome_driver


@pytest.fixture()
def customer_account_create_page(driver):
    """Fixture to initialize the CustomerAccountCreatePage instance."""
    return CustomerAccountCreatePage(driver)


@pytest.fixture()
def eco_friendly_page(driver):
    """Fixture to initialize the EcoFriendlyPage instance."""
    return EcoFriendlyPage(driver)


@pytest.fixture()
def sale_page(driver):
    """Fixture to initialize the SalePage instance."""
    return SalePage(driver)
