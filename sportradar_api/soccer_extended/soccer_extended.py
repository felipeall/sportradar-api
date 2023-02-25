from dataclasses import dataclass

from sportradar_api.main import SportradarAPI


@dataclass
class SoccerExtended(SportradarAPI):
    """Wrapper to interact with Sportradar SoccerExtended API"""

    api: str = "soccer-extended"

    def get_competitions(self) -> dict:
        """Get all available Soccer competitions.

        Returns:
            API response
        """
        return self._call_endpoint(endpoint="competitions", key="competitions")

    def get_seasons(self) -> dict:
        """Get historical season information for all competitions.

        Returns:
            API response
        """
        return self._call_endpoint(endpoint="seasons", key="seasons")

    def get_season_summaries(self, season_urn: str) -> dict:
        """Get the summaries for all sport events in a season (any status). Provides information for all matches from a
        given season including scoring and statistics at the match level.

        Args:
            season_urn:

        Returns:
            API response
        """
        return self._call_endpoint(endpoint=f"seasons/{season_urn}/summaries", key="summaries")

    def get_season_competitors(self, season_urn: str) -> dict:
        """Get all teams participating for a given season.

        Args:
            season_urn: URN of a given season

        Returns:
            API response
        """
        return self._call_endpoint(endpoint=f"seasons/{season_urn}/competitors", key="season_competitors")

    def get_player_profile(self, player_urn: str) -> dict:
        """Get the player profile for the given urn. Provides player information, including current and historical team
        membership info.

        Args:
            player_urn: URN of a given player

        Returns:
            API response
        """

        return self._call_endpoint(endpoint=f"players/{player_urn}/profile")
