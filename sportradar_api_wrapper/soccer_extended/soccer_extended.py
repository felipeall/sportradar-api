from dataclasses import dataclass

from sportradar_api_wrapper.main import SportradarAPI


@dataclass
class SoccerExtended(SportradarAPI):
    api: str = "soccer-extended"

    def get_competitions(self) -> dict:
        return self._call_endpoint(endpoint="competitions", key="competitions")

    def get_seasons(self) -> dict:
        return self._call_endpoint(endpoint="seasons", key="seasons")

    def get_season_summary(self, season_urn: str) -> dict:
        return self._call_endpoint(endpoint=f"seasons/{season_urn}/summaries", key="summaries")

    def get_season_competitors(self, season_urn: str) -> dict:
        return self._call_endpoint(endpoint=f"seasons/{season_urn}/competitors", key="season_competitors")
