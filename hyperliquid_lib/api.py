import json
import logging
from json import JSONDecodeError

import requests
from requests.adapters import HTTPAdapter

from hyperliquid_lib.utils.error import ClientError, ServerError
from hyperliquid_lib.utils.types import Any
from fake_useragent import UserAgent

class API:
    def __init__(self, proxies=None):
        self.base_url = "https://api.hyperfoundation.org"
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "Origin": "https://api.hyperfoundation.org",
            "Referer": "https://api.hyperfoundation.org/",
            "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"macOS"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
        })
        self.user_agent = UserAgent()
        if proxies:
            self._configure_adapter(proxies)

    def _configure_adapter(self, proxies):
        adapter = HTTPAdapter(
            pool_connections=170,
            pool_maxsize=170,
            max_retries=3
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        # Hardcoded proxies with authentication
        self.session.proxies.update({
            "http": proxies,
            "https": proxies
        })

    

    def post(self, url_path: str, payload: Any = None) -> Any: # type: ignore
        payload = payload or {}
        url = self.base_url + url_path
        self.session.headers.update({
            "User-Agent": self.user_agent.random
        })
        response = self.session.post(url, json=payload)
        self._handle_exception(response)
        try:
            return response.json()
        except ValueError:
            return {"error": f"Could not parse JSON: {response.text}"}

    def _handle_exception(self, response):
        status_code = response.status_code
        if status_code < 400:
            return
        if 400 <= status_code < 500:
            try:
                err = json.loads(response.text)
            except JSONDecodeError:
                raise ClientError(status_code, None, response.text, None, response.headers)
            if err is None:
                raise ClientError(status_code, None, response.text, None, response.headers)
            error_data = err.get("data")
            raise ClientError(status_code, err["code"], err["msg"], response.headers, error_data)
        raise ServerError(status_code, response.text)
