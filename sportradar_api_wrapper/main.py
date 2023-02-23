from dataclasses import dataclass
from time import sleep

import requests
from requests import Response, HTTPError


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

    def _call_endpoint(self, endpoint: str, key: str) -> dict:
        response = self._make_request(endpoint=endpoint)
        content = response.json()

        request_results = response.headers.get("X-Result")
        request_results_max = response.headers.get("X-Max-Results")

        if request_results is None or request_results_max is None:
            return content

        request_results = int(request_results)
        request_results_max = int(request_results_max)

        if request_results_max - request_results <= 0:
            return content

        for offset in range(request_results, request_results_max, request_results):
            response = self._make_request(endpoint=endpoint, offset=offset, limit=request_results)
            content[key].extend(response.json().get(key))

        return content

    def _make_request(self, endpoint: str, offset: int = 0, limit: int = 0) -> Response:
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

        print(f"[{endpoint}] Calling endpoint...")
        print(f"[{endpoint}] {offset=} {limit=}")

        response = requests.get(
            url,
            timeout=self.timeout,
            params={"api_key": self.api_key, "offset": offset, "limit": limit},
        )

        print(f"[{endpoint}] Status code: 200")
        print(
            f"[{endpoint}] API Key Status: "
            f"{response.headers.get('X-Plan-Quota-Current')}"
            f"/{response.headers.get('X-Plan-Quota-Allotted')}"
        )

        if response.status_code == 200:
            return response

        elif 400 <= response.status_code < 500:
            raise HTTPError(f"{response.status_code} Client Error: {response.reason} for url: {url}", response=response)

        elif 500 <= response.status_code < 600:
            raise HTTPError(f"{response.status_code} Server Error: {response.reason} for url: {url}", response=response)
