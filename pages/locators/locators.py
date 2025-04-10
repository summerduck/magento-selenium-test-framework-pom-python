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
    pass


class CreateAccountPageLocators(object):
    pass


class CreateAccountSuccessPageLocators(object):
    pass
