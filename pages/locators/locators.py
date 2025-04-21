"""
Locators module for the Magento test framework.
"""

from selenium.webdriver.common.by import By


class CustomerAccountCreatePageLocators(object):
    """
    Locators for the Customer Account Create Page.
    """

    # Form locators
    FIRSTNAME_INPUT = (By.ID, "firstname")
    LASTNAME_INPUT = (By.ID, "lastname")
    EMAIL_INPUT = (By.ID, "email_address")
    PASSWORD_INPUT = (By.ID, "password")
    PASSWORD_CONFIRM_INPUT = (By.ID, "password-confirmation")

    # Submit button locator
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[title='Create an Account']")

    # Error locators
    FIRSTNAME_ERROR = (By.ID, "firstname-error")
    LASTNAME_ERROR = (By.ID, "lastname-error")
    EMAIL_ERROR = (By.ID, "email_address-error")
    PASSWORD_ERROR = (By.ID, "password-error")
    PASSWORD_CONFIRM_ERROR = (By.ID, "password-confirmation-error")

    # Password strength meter locators
    PASSWORD_STRENGTH_METER = (By.ID, "password-strength-meter-container")
    PASSWORD_STRENGTH_METER_LABEL = (By.ID, "password-strength-meter-label")
    PASSWORD_ERROR = (By.ID, "password-error")


class EcoFriendlyPageLocators(object):
    """
    Locators for the Eco-Friendly Page.
    """

    # Page title and main content locators
    PAGE_TITLE = (By.ID, "page-title-heading")
    PRODUCT_GRID = (By.CSS_SELECTOR, ".products-grid")
    PRODUCT_LIST = (By.CSS_SELECTOR, ".products-list")

    # Mode switch locators
    GRID_MODE = (By.CSS_SELECTOR, ".modes-mode.mode-grid")
    LIST_MODE = (By.CSS_SELECTOR, ".modes-mode.mode-list")

    ACTIVE_GRID_MODE = (By.CSS_SELECTOR, ".modes-mode.active.mode-grid")
    ACTIVE_LIST_MODE = (By.CSS_SELECTOR, ".modes-mode.active.mode-list")

    # Product list locators
    PRODUCT_ITEMS_LIST = (By.CLASS_NAME, "products wrapper grid products-grid")
    PRODUCT_ITEM = (By.CLASS_NAME, "product-item-info")
    PRODUCT_NAME = (By.CSS_SELECTOR, ".product-item-link")
    PRODUCT_PRICE = (By.CLASS_NAME, "price-wrapper ")

    # Toolbar locators
    TOOLBAR = (By.CSS_SELECTOR, ".toolbar.toolbar-products")
    SORT_BY_DROPDOWN = (By.ID, "sorter")
    SHOW_PER_PAGE_DROPDOWN = (By.XPATH, "(//select[@id='limiter'])[2]")
    SHOW_PER_PAGE_DROPDOWN_OPTION = (
        By.XPATH,
        "(//select[@id='limiter'])[2]//option[text()='%s']",
    )
    TOOLBAR_AMOUNT = (By.CSS_SELECTOR, "#toolbar-amount")
    TOTAL_PRODUCTS_COUNT = (By.CSS_SELECTOR, ".toolbar-amount span:last-child")

    # Product action locators
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button.action.tocart.primary")
    ADD_TO_WISHLIST_BUTTON = (By.CSS_SELECTOR, ".action.towishlist")
    ADD_TO_COMPARE_BUTTON = (By.CSS_SELECTOR, ".action.tocompare")


class SalePageLocators(object):
    """
    Locators for the Sale Page.
    """

    PAGE_TITLE = (By.ID, "page-title-heading")

    # Deal section locators
    WOMENS_DEALS_SECTION = (By.XPATH, "//span[contains(text(),'Women's Deals')]")
    MENS_DEALS_SECTION = (By.XPATH, "//span[contains(text(),'Men's Deals')]")
    GEAR_DEALS_SECTION = (By.XPATH, "//span[contains(text(),'Gear Deals')]")

    # Promotional content locators
    PROMO_BANNERS = (By.CLASS_NAME, "blocks-promo")
    DISCOUNT_BANNER = (By.XPATH, "//a[@class='block-promo sale-20-off']")
    FREE_SHIPPING_BANNER = (By.XPATH, "//a[@class='block-promo sale-free-shipping']")
    TEES_PROMO = (By.XPATH, "//a[@class='block-promo sale-womens-t-shirts']")

    # Product category links
    WOMENS_CATEGORIES = (By.CSS_SELECTOR, ".women-deals a")
    MENS_CATEGORIES = (By.CSS_SELECTOR, ".mens-deals a")
    GEAR_CATEGORIES = (By.CSS_SELECTOR, ".gear-deals a")
