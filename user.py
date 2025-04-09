import random
import string
from enum import Enum
from dataclasses import dataclass
from typing import List


@dataclass
class UserData:
    """User data structure for test automation"""
    first_name: str
    last_name: str
    email: str


class UserRandom(Enum):
    """Enum for generating random user test data"""
    
    # Common test users
    DEFAULT = UserData(
        first_name="Test",
        last_name="User",
        email="testuser@example.com"
    )
    
    ADMIN = UserData(
        first_name="Admin",
        last_name="User",
        email="admin@example.com"
    )
    
    GUEST = UserData(
        first_name="Guest",
        last_name="User",
        email="guest@example.com"
    )
    
    @classmethod
    def random(cls) -> UserData:
        """Generate a random user with randomized data"""
        first_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8)).capitalize()
        last_name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8)).capitalize()
        email = f