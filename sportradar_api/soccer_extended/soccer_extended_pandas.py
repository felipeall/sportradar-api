from dataclasses import dataclass

import pandas as pd
from flatten_json import flatten

from sportradar_api import SoccerExtended


@dataclass
class SoccerExtendedPandas:
    """Parser to transform the SoccerExtended API response to Pandas DataFrame"""

    api_key: str
    quiet: bool = True

    def __post_init__(self):
        self.soccer_extended = SoccerExtended(api_key=self.api_key, quiet=self.quiet)

    def get_competitions(self) -> pd.DataFrame:
        """Get all available Soccer competitions.

        Returns:
            Pandas DataFrame
        """
        competitions = self.soccer_extended.get_competitions()
        competitions = pd.json_normalize(competitions["competitions"])

        return competitions

    def get_seasons(self) -> pd.DataFrame:
        """Get historical season information for all competitions.

        Returns:
            Pandas DataFrame
        """
        seasons = self.soccer_extended.get_seasons()
        seasons = pd.json_normalize(seasons["seasons"])

        return seasons

    def get_season_competitors(self, season_urn: str) -> pd.DataFrame:
        """Get all teams participating for a given season.

        Args:
            season_urn: URN of a given season

        Returns:
            Pandas DataFrame
        """
        season_competitors = self.soccer_extended.get_season_competitors(season_urn=season_urn)
        season_competitors = pd.json_normalize(season_competitors["season_competitors"])

        return season_competitors.assign(season_urn=season_urn)

    def get_player_profile_info(self, player_urn: str) -> pd.DataFrame:
        """Get the basic information from a player profile

        Args:
            player_urn: URN of a given player

        Returns:
            Pandas DataFrame
        """
        player_profile = self.soccer_extended.get_player_profile(player_urn=player_urn)
        player_profile_info = pd.json_normalize(player_profile["player"])

        return player_profile_info.assign(player_id=player_urn)

    def get_player_profile_competitors(self, player_urn: str) -> pd.DataFrame:
        """Get the competitors from a player profile

        Args:
            player_urn: URN of a given player

        Returns:
            Pandas DataFrame
        """
        player_profile = self.soccer_extended.get_player_profile(player_urn=player_urn)
        player_profile_competitors = pd.json_normalize(player_profile["competitors"])

        return player_profile_competitors.assign(player_id=player_urn)

    def get_player_profile_roles(self, player_urn: str) -> pd.DataFrame:
        """Get the roles from a player profile

        Args:
            player_urn: URN of a given player

        Returns:
            Pandas DataFrame
        """
        player_profile = self.soccer_extended.get_player_profile(player_urn=player_urn)
        player_profile_roles = pd.json_normalize([flatten(role, separator=".") for role in player_profile["roles"]])

        return player_profile_roles.assign(player_urn=player_urn)
