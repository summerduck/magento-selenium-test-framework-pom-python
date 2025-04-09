"""Pytest configuration file for Selenium tests with fixture definitions."""

import logging
import os
import re
import shutil
import sys
import random
from typing import Generator
from dotenv import load_dotenv

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver
from pages.customer_account_create_page import CustomerAccountCreatePage
from pages.eco_friendly_page import EcoFriendlyPage
from pages.sale_page import SalePage

# Handle display of output log when using xdist
sys.stdout = sys.stderr

# Base directory for test logs
LOG_DIR = "test-logs"
FAILED_LOG_DIR = os.path.join(LOG_DIR, "failed_tests")

# Initialize logger
logger = logging.getLogger(__name__)


@pytest.fixture()
def driver():
    """Fixture to initialize the Chrome driver with necessary options."""
    options = Options()
    # options.add_argument("--headless")
    # options.add_argument("--auto-open-devtools-for-tabs")
    chrome_driver = webdriver.Chrome(options=options)
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture()
def customer_account_create_page(driver: WebDriver):
    """Fixture to initialize the CustomerAccountCreatePage instance."""
    return CustomerAccountCreatePage(driver)


@pytest.fixture()
def eco_friendly_page(driver: WebDriver):
    """Fixture to initialize the EcoFriendlyPage instance."""
    return EcoFriendlyPage(driver)


@pytest.fixture()
def sale_page(driver: WebDriver):
    """Fixture to initialize the SalePage instance."""
    return SalePage(driver)


# Pytest custom add option arguments
def pytest_addoption(parser):
    """
    Pytest custom arguments
    :param parser:
    :return:
    """
    # Load the .env file
    load_dotenv()
    parser.addoption(
        "--user-pw",
        action="store",
        help="USER_PASSWORD",
        default=os.getenv("USER_PASSWORD"),
    )


def make_dir_for_logs():
    """
    Create directory for logs. Delete exists
    :return:
    """
    # Check if the directory exists before attempting to delete it
    if os.path.exists(LOG_DIR):
        # Delete the directory and its contents
        shutil.rmtree(LOG_DIR)

    # Create a new log directory
    os.makedirs(LOG_DIR, exist_ok=True)
    os.makedirs(FAILED_LOG_DIR, exist_ok=True)


def pytest_configure(config):
    """
    Pytest configuration setup
    :param config:
    :return:
    """
    make_dir_for_logs()


@pytest.fixture
def user_password(request):
    """
    Argument for tc diner user password
    :param request:
    :return:
    """
    return request.config.getoption("--user-pw")


def sanitize_nodeid(node_id):
    """
    Cleans up and formats the test's nodeid
    (a unique identifier for each test in Pytest).
    """
    tokens = node_id.split("::")
    tokens[-1] = tokens[-1].replace("/", "-")
    tokens[-1] = re.sub(r"-+", "-", tokens[-1])
    node_id = "/".join([x for x in tokens if x != "()"])
    node_id = re.sub(r"\[(.+)\]", r"-\1", node_id)
    return node_id


def get_last_element(node_id):
    """
    Retrieves the last part of the sanitized nodeid,
    which represents the specific test name.
    """
    return node_id.split("/")[-1]


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    """
    Configures a unique logger for each test before it runs
    """
    # Get test node ID for log naming
    test_name = get_last_element(sanitize_nodeid(item.nodeid))
    max_filename_length = 255
    truncated_test_name = test_name[
        : max_filename_length - len(LOG_DIR) - 5
    ]  # 5 for ".log" and separators
    log_file = os.path.join(LOG_DIR, f"{truncated_test_name}.log")

    # Configure logging for the current test
    logger = logging.getLogger()
    logger.handlers = []  # Remove any existing handlers
    handler = logging.FileHandler(log_file)
    formatter = logging.Formatter("%(asctime)s [%(levelname)s] [%(name)s] %(message)s")
    formatter.default_msec_format = "%s.%03d"
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    logger.info("Starting test - %s", item.nodeid)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_teardown(item, nextitem):
    """
    leans up the logger after the test is completed
    """
    logger = logging.getLogger()
    logger.info("Finished test - %s", item.nodeid)

    # Remove test-specific handlers
    for handler in logger.handlers[:]:
        if isinstance(handler, logging.FileHandler):
            handler.close()
            logger.removeHandler(handler)


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logreport(report):
    """
    Handles special processing for logs of failed tests
    """
    if report.when == "call" and report.failed:
        test_name = get_last_element(sanitize_nodeid(report.nodeid))
        log_file = os.path.join(LOG_DIR, f"{test_name}.log")
        failed_log_file = os.path.join(FAILED_LOG_DIR, f"{test_name}.log")
        if os.path.exists(log_file):
            os.rename(log_file, failed_log_file)
