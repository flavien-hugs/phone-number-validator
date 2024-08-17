import logging
from typing import Optional
from urllib.parse import urljoin

import httpx
from .config.url_patterns import API_BASE_URL

logging.basicConfig(format="%(message)s", level=logging.INFO)
_log = logging.getLogger(__name__)


class PhoneNumberValidator:
    def __init__(self, api_key: str) -> None:
        """
        Initializes the PhoneNumberValidator class with an API key.

        :param api_key: Your API key for the NumLookupAPI.
        :type api_key: str
        """
        self.api_key = api_key
        self.api_url = API_BASE_URL

    async def _make_api_call(self, phone_number: str, country_code: Optional[str] = None) -> httpx.Response:
        """
        Makes an API call to the NumLookupAPI to validate a phone number.

        :param phone_number: The phone number you want to validate.
        :type phone_number: str
        :param country_code: An ISO Alpha 2 Country Code for the phone number (e.g. "CI").
        :type country_code: str
        :return: The response object returned by the API call.
        :rtype: httpx.Response
        """

        params = {"apikey": self.api_key}
        if country_code:
            params["country_code"] = country_code
        url = urljoin(self.api_url, phone_number)

        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, params=params)

        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            _log.info(f"HTTP error occurred: {exc.response.status_code}")
            raise
        except httpx.RequestError as exc:
            _log.info(f"An error occurred while requesting {exc.request.url}: {exc}")
            raise

        return response

    async def validate(self, phone_number: str, country_code: Optional[str] = None) -> bool:
        """
        Validates a phone number using the NumLookupAPI.

        :param phone_number: The phone number you want to validate.
        This can either include the country prefix (e.g. "+1 650-253-0000") or not (e.g. "650-253-0000").
        If the `country_code` argument is not provided, the API will try to detect the country automatically.
        :type phone_number: str
        :param country_code: n ISO Alpha 2 Country Code for the phone number (e.g. "US"). If this argument is provided,
        the API will use it to validate the phone number. If not provided, the API will try to detect the country
        automatically based on the phone number.
        :type country_code: str
        :return: True if the phone number is valid, False otherwise.
        :rtype: bool
        :raises ValueError: If the phone number is empty.

        .. code-block:: python example usage
            validator = PhoneNumberValidator(api_key="your_api_key")
            valid = await validator.validate(phone_number="+1 650-253-0000")
            print(valid)
            True

        In this example, the phone number "+1 650-253-0000" is validated.
        The API automatically detects that the country code is "US" based on the "+1" prefix.
        The function returns `True` if the phone number is valid.
        """

        if not phone_number:
            raise ValueError("Phone number cannot be empty")

        response = await self._make_api_call(phone_number=phone_number, country_code=country_code)
        result = response.json()["valid"] if response.is_success else False
        return result
