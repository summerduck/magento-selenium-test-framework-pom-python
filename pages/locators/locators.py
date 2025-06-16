"""
Locators module for the Magento test framework.
"""

from selenium.webdriver.common.by import By


class CustomerAccountCreatePageLocators:
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


class EcoFriendlyPageLocators:
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


class SalePageLocators:
    """
    Locators for the Sale Page.
    """

    PAGE_TITLE = (By.ID, "page-title-heading")

    # Deal section locators
    CATEGORIES_MENU = (By.XPATH, "//div[@class='categories-menu']")
    WOMENS_DEALS_MENU_CATEGORY = (
        By.XPATH,
        '//strong[@class="title"]//span[text()="Women\'s Deals"]',
    )
    MENS_DEALS_MENU_CATEGORY = (
        By.XPATH,
        '//strong[@class="title"]//span[text()="Mens\'s Deals"]',
    )
    GEAR_DEALS_MENU_CATEGORY = (
        By.XPATH,
        "//strong[@class='title']//span[text()='Gear Deals']",
    )

    # Promotional content locators
    PROMO_BANNERS = (By.CLASS_NAME, "blocks-promo")
    DISCOUNT_BANNER = (By.XPATH, "//a[@class='block-promo sale-20-off']")
    FREE_SHIPPING_BANNER = (By.XPATH, "//a[@class='block-promo sale-free-shipping']")
    TEES_PROMO = (By.XPATH, "//a[@class='block-promo sale-womens-t-shirts']")

    # Product category links
    WOMENS_CATEGORIES = (
        By.XPATH,
        '(//strong[@class="title"][span[text()="Women\'s Deals"]]/following-sibling::ul[@class="items"])[1]//li//a',
    )
    MENS_CATEGORIES = (
        By.XPATH,
        '(//strong[@class="title"][span[text()="Mens\'s Deals"]]/following-sibling::ul[@class="items"])[1]//li//a',
    )
    GEAR_CATEGORIES = (
        By.XPATH,
        '//strong[@class="title"][span[text()="Gear Deals"]]/following-sibling::ul[@class="items"]//li//a',
    )
