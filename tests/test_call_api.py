from unittest import mock

import httpx
import pytest
from faker import Faker

f = Faker()


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", [f"+225015157139{i}" for i in range(3)])
async def test_make_api_call_success(mock_validator, httpx_mock, phone_number):
    mock_validator._make_api_call = mock.AsyncMock(
        return_value=httpx.Response(status_code=200, json={"valid": True})
    )
    response = await mock_validator._make_api_call(phone_number)

    assert response.status_code == 200
    assert response.json() == {"valid": True}

    mock_validator._make_api_call.assert_awaited()
    mock_validator._make_api_call.assert_awaited_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", [f"+225015157139{i}" for i in range(2)])
async def test_make_api_call_http_error(mock_validator, phone_number):
    with mock.patch(
            "httpx.AsyncClient.get",
            side_effect=httpx.RequestError("Network error", request=mock.AsyncMock())
    ) as mock_client:
        with pytest.raises(httpx.RequestError):
            await mock_validator._make_api_call(phone_number)

    mock_client.assert_awaited()
    mock_client.assert_called_once()


@pytest.mark.asyncio
@pytest.mark.parametrize("phone_number", [f"+225015157139{i}" for i in range(2)])
async def test_make_api_call_status_error(mock_validator, httpx_mock, phone_number):
    httpx_mock.add_response(status_code=404)

    with pytest.raises(httpx.HTTPStatusError):
        response = await mock_validator._make_api_call(phone_number)
        assert response.status_code == 404
        assert response.is_success is False
