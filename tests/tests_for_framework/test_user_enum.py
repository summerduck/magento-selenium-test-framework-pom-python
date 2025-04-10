import os
import pytest
from data.users import User, UserData


@pytest.fixture(autouse=True)
def setup_env():
    """Ensure USER_PASSWORD is set in environment"""
    if "USER_PASSWORD" not in os.environ:
        os.environ["USER_PASSWORD"] = "TestPassword123!"


class UsersDataTest:
    """Test class for User enum"""

    def test_standard_user_data(self):
        """Test standard user creation"""
        user = User.STANDARD
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.email == "john.doe@example.com"
        assert user.password == os.getenv("USER_PASSWORD")

    def test_random_user(self):
        """Test random user generation"""
        user = User.random()
        assert isinstance(user, UserData)
        assert isinstance(user.first_name, str)
        assert isinstance(user.last_name, str)
        assert isinstance(user.email, str)
        assert "@" in user.email  # Basic email validation
        assert user.password == os.getenv("USER_PASSWORD")

    def test_custom_email_user(self):
        """Test user creation with custom email"""
        custom_email = "test@custom.com"
        user = User.with_custom_email(custom_email)
        assert isinstance(user, UserData)
        assert user.email == custom_email
        assert user.password == os.getenv("USER_PASSWORD")

    def test_custom_name_user(self):
        """Test user creation with custom name components"""
        first_name = "Alice"
        last_name = "Smith"

        # Test with both names
        user1 = User.with_custom_name(first_name=first_name, last_name=last_name)
        assert user1.first_name == first_name
        assert user1.last_name == last_name

        # Test with only first name
        user2 = User.with_custom_name(first_name=first_name)
        assert user2.first_name == first_name
        assert isinstance(user2.last_name, str)

        # Test with only last name
        user3 = User.with_custom_name(last_name=last_name)
        assert isinstance(user3.first_name, str)
        assert user3.last_name == last_name

    def test_custom_password(self):
        """Test user creation with custom password"""
        password = "CustomPassword123!"
        user = User.with_custom_password(password)
        assert user.password == password

    def test_custom_domain_email_user(self):
        """Test user creation with same domain email"""
        domain = "company.test"
        user = User.with_same_domain_email(domain)
        assert isinstance(user, UserData)
        assert user.email.endswith(f"@{domain}")
        assert user.email.startswith(
            f"{user.first_name.lower()}.{user.last_name.lower()}"
        )

    def test_multiple_random_users_are_different(self):
        """Test that multiple random users have different data"""
        user1 = User.random()
        user2 = User.random()
        assert (
            user1.first_name != user2.first_name
            or user1.last_name != user2.last_name
            or user1.email != user2.email
        )
