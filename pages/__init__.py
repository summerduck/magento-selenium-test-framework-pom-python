"""
Page objects module for the Magento test framework.
"""

from .base_page import BasePage
from .customer_account_create_page import CustomerAccountCreatePage
from .eco_friendly_page import EcoFriendlyPage
from .sale_page import SalePage

__all__ = [
    "BasePage",
    "CustomerAccountCreatePage",
    "EcoFriendlyPage",
    "SalePage",
]
