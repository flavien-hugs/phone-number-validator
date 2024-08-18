import pytest

from phone_number_validator.validator import PhoneNumberValidator


@pytest.fixture
def mock_validator():
    return PhoneNumberValidator(api_key="test_api_key")
