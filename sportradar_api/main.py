import logging
from dataclasses import dataclass
from time import sleep
from typing import Optional

import requests
from requests import HTTPError, Response


@dataclass
class SportradarAPI:
    api_key: str
    api: str
    api_access_level: str = "trial"
    api_version: str = "v4"
    api_language_code: str = "en"
    api_format: str = "json"
    timeout: int = 120
    sleep_time: int = 1.2
    quiet: bool = True

    def __post_init__(self):
        if not self.quiet:
            logging.basicConfig(
                level=logging.INFO,
                format="[%(asctime)s] [SportradarAPI] %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
        self.log = logging.getLogger()

    def _call_endpoint(self, endpoint: str, key: Optional[str] = None) -> dict:
        response = self._make_request(endpoint=endpoint)
        content = response.json()

        request_results = response.headers.get("X-Result")
        request_max_results = response.headers.get("X-Max-Results")
        self.log.info(f"[{endpoint}] Headers: {response.headers}")

        if request_results is None or request_max_results is None:
            self.log.info(f"[{endpoint}] Fetching complete!")
            return content

        request_results = int(request_results)
        request_max_results = int(request_max_results)

        if request_max_results - request_results <= 0:
            self.log.info(f"[{endpoint}] Total records: {len(content.get(key))}")
            self.log.info(f"[{endpoint}] Fetching complete!")
            return content

        for offset in range(request_results, request_max_results, request_results):
            response = self._make_request(endpoint=endpoint, offset=offset, limit=request_results)
            content[key].extend(response.json().get(key))

        self.log.info(f"[{endpoint}] Parsed records: {len(content.get(key))}")
        self.log.info(f"[{endpoint}] Fetching complete!")
        return content

    def _make_request(self, endpoint: str, offset: Optional[int] = None, limit: Optional[int] = None) -> Response:
        sleep(self.sleep_time)

        url = (
            "https://api.sportradar.us"
            f"/{self.api}"
            f"/{self.api_access_level}"
            f"/{self.api_version}"
            f"/{self.api_language_code}"
            f"/{endpoint}"
            f".{self.api_format}"
        )

        self.log.info(f"[{endpoint}] Calling endpoint...")
        self.log.info(f"[{endpoint}] Parameters: {offset=} {limit=}")

        response = requests.get(
            url,
            timeout=self.timeout,
            params={"api_key": self.api_key, "offset": offset, "limit": limit},
        )

        self.log.info(f"[{endpoint}] Response Status Code: {response.status_code}")
        self.log.info(
            f"[{endpoint}] Updated API Key Quota: "
            f"{response.headers.get('X-Plan-Quota-Current')}"
            f"/{response.headers.get('X-Plan-Quota-Allotted')}"
        )

        if response.status_code == 200:
            return response

        elif 400 <= response.status_code < 500:
            raise HTTPError(f"{response.status_code} Client Error: {response.reason} for url: {url}", response=response)

        elif 500 <= response.status_code < 600:
            raise HTTPError(f"{response.status_code} Server Error: {response.reason} for url: {url}", response=response)
