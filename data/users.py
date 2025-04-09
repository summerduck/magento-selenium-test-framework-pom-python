"""
This file contains the UserRandom class, which is used to create a user with random data.
And User enum, which is used to create a user with predefined data.
"""

import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from faker import Faker

fake = Faker()
load_dotenv()


@dataclass
class UserData:
    """Class for storing user data"""

    first_name: str
    last_name: str
    email: str
    password: str


class User:
    """Class for generating user data for automation tests using Faker.

    This class provides methods to create users with:
    - Standard predefined data (STANDARD)
    - Random data (random())
    - Custom email (with_custom_email())
    - Custom name components (with_custom_name())
    """

    STANDARD = UserData(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password=os.getenv("USER_PASSWORD"),
    )

    ADMIN = UserData(
        first_name="Admin",
        last_name="Admin",
        email="admin@example.com",
        password=os.getenv("USER_PASSWORD"),
    )

    @classmethod
    def random(cls) -> UserData:
        """Generate completely random user data"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()

        return UserData(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=os.getenv("USER_PASSWORD"),
        )

    @classmethod
    def with_custom_email(cls, email: str) -> UserData:
        """Generate random user with custom email"""
        return UserData(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=email,
            password=os.getenv("USER_PASSWORD"),
        )

    @classmethod
    def with_custom_name(
        cls, first_name: Optional[str] = None, last_name: Optional[str] = None
    ) -> UserData:
        """Generate random user with custom name components"""
        first = first_name or fake.first_name()
        last = last_name or fake.last_name()

        return UserData(
            first_name=first,
            last_name=last,
            email=fake.email(),
            password=os.getenv("USER_PASSWORD"),
        )

    @classmethod
    def with_same_domain_email(cls, domain: str = "testcompany.com") -> UserData:
        """Generate random user with email at specified domain"""
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f"{first_name.lower()}.{last_name.lower()}"
        email = f"{username}@{domain}"

        return UserData(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=os.getenv("USER_PASSWORD"),
        )


user = User.STANDARD
print(isinstance(user, UserData))
# True
random_user = User.random()
print(isinstance(random_user, UserData))
# True
