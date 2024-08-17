import pytest
from phone_number_validator.validator import PhoneNumberValidator

from faker import Faker


@pytest.fixture
def mock_validator():
    return PhoneNumberValidator(api_key="test_api_key")
