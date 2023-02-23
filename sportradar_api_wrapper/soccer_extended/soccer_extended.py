from dataclasses import dataclass
from time import sleep
from typing import Optional

import requests


@dataclass
class SoccerExtended:
    api_key: str
    api: str = "soccer-extended"
    api_access_level: str = "trial"
    api_version: str = "v4"
    api_language_code: str = "en"
    api_format: str = "json"
    offset: int = 0
    limit: int = 0
    timeout: int = 120
    sleep_time: int = 1.1

    def get_competitions(self):
        return self._call_endpoint("competitions")

    def get_season_summary(self, season_urn: str):
        endpoint = f"seasons/{season_urn}/summaries"

        response = self._call_endpoint(endpoint=endpoint)

        if self.offset == 0 and self.limit == 0:
            r, offset, limit = [0], 200, 400
            while r:
                r = self._call_endpoint(endpoint=endpoint, offset=offset, limit=limit).get("summaries")
                response["summaries"].extend(r)
                offset += 200
                limit += 200

        return response

    def _call_endpoint(self, endpoint: str, offset=None, limit=None) -> Optional[dict]:
        if not offset:
            offset = self.offset
        if not limit:
            limit = self.limit

        sleep(self.sleep_time)
        url = f"http://api.sportradar.us/{self.api}/{self.api_access_level}/{self.api_version}/{self.api_language_code}/{endpoint}.{self.api_format}"

        print(f"[{endpoint}] {offset=} {limit=}")
        print(f"[{endpoint}] Calling endpoint...")

        response = requests.get(url, timeout=self.timeout, params={"api_key": self.api_key, "offset": offset, "limit": limit})

        print(f"[{endpoint}] Status code: 200")

        if response.status_code == 200:
            return response.json()
        else:
            return None
