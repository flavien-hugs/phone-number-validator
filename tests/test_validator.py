from unittest import mock

import httpx
import pytest
from faker import Faker

f = Faker()


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", [f"+225015157139{i}" for i in range(2)])
async def test_valid_phone_number(mock_validator, httpx_mock, phone_number):
    mock_validator._make_api_call = mock.AsyncMock(
        return_value=httpx.Response(status_code=200, json={"valid": True})
    )
    valid = await mock_validator.validate(phone_number)
    assert valid is True
    mock_validator._make_api_call.assert_called_once()
    mock_validator._make_api_call.assert_called_with(
        phone_number=phone_number, country_code=None
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", [f"+225015157139{i}" for i in range(2)])
async def test_invalid_phone_number(mock_validator, httpx_mock, phone_number):
    mock_validator._make_api_call = mock.AsyncMock(
        return_value=httpx.Response(status_code=200, json={"valid": False})
    )
    valid = await mock_validator.validate(phone_number)
    assert valid is False
    mock_validator._make_api_call.assert_called_once()
    mock_validator._make_api_call.assert_called_with(
        phone_number=phone_number, country_code=None
    )


@pytest.mark.asyncio
async def test_empty_phone_number(mock_validator):
    with pytest.raises(ValueError, match="Phone number cannot be empty"):
        await mock_validator.validate("")
