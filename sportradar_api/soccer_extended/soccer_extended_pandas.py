from dataclasses import dataclass

import pandas as pd
from flatten_json import flatten

from sportradar_api import SoccerExtended
from sportradar_api.main import SportradarAPI
from sportradar_api.utils.utils import (
    explode_column,
    remove_cols_str,
    remove_str,
    replace_cols_str,
)


@dataclass
class SoccerExtendedPandas(SportradarAPI):
    """Parser to transform the SoccerExtended API response to Pandas DataFrame"""

    api: str = "soccer-extended"

    def __post_init__(self):
        self.soccer_extended = SoccerExtended(api_key=self.api_key, verbose=self.verbose)

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

    def get_season_matches(self, season_urn: str):
        """Get the information of all matches from a given season.

        Args:
            season_urn: URN of a given season

        Returns:
            Pandas DataFrame
        """
        cols = [
            "sport_event.id",
            "sport_event.start_time",
            "sport_event.start_time_confirmed",
            "sport_event.sport_event_context.sport.id",
            "sport_event.sport_event_context.category.id",
            "sport_event.sport_event_context.competition.id",
            "sport_event.sport_event_context.season.id",
            "sport_event.coverage.sport_event_properties.lineups",
            "sport_event.coverage.sport_event_properties.venue",
            "sport_event.coverage.sport_event_properties.extended_player_stats",
            "sport_event.coverage.sport_event_properties.extended_team_stats",
            "sport_event.coverage.sport_event_properties.basic_play_by_play",
            "sport_event.coverage.sport_event_properties.basic_player_stats",
            "sport_event.coverage.sport_event_properties.basic_team_stats",
            "sport_event.competitor_home_id",
            "sport_event.competitor_away_id",
            "sport_event.venue.id",
            "sport_event.sport_event_conditions.ground.neutral",
            "sport_event_status.status",
            "sport_event_status.match_status",
            "sport_event.replaced_by",
            "sport_event_status.home_score",
            "sport_event_status.away_score",
            "sport_event_status.match_tie",
            "sport_event_status.winner_id",
        ]
        season_summaries = self.soccer_extended.get_season_summaries(season_urn=season_urn)
        season_matches = pd.json_normalize(season_summaries["summaries"])

        competitors = pd.DataFrame(season_matches.pop("sport_event.competitors").to_list())
        competitors.columns = ["sport_event.competitor_home_id", "sport_event.competitor_away_id"]
        competitors["sport_event.competitor_home_id"] = competitors["sport_event.competitor_home_id"].apply(
            lambda x: x.get("id")
        )
        competitors["sport_event.competitor_away_id"] = competitors["sport_event.competitor_away_id"].apply(
            lambda x: x.get("id")
        )

        cols_select = [col for col in cols if col in season_matches.columns]

        season_matches = (
            season_matches.join(competitors)
            .loc[:, cols_select]
            .pipe(
                remove_cols_str,
                [
                    "sport_event.",
                    "sport_event_context.",
                    "coverage.sport_event_properties.",
                    "sport_event_conditions.",
                    "sport_event_status.",
                ],
            )
            .pipe(replace_cols_str, {".": "_"})
        )

        return season_matches

    def get_season_matches_statistics(self, season_urn: str) -> pd.DataFrame:
        """Get the players statistics of all matches from a given season.

        Args:
            season_urn: URN of a given season

        Returns:
            Pandas DataFrame
        """
        season_summaries = self.soccer_extended.get_season_summaries(season_urn=season_urn)

        matches_statistics = (
            pd.json_normalize(season_summaries, "summaries")
            .pipe(explode_column, "statistics.totals.competitors", ["sport_event.id", "sport_event.start_time"])
            .pipe(
                explode_column,
                "statistics.totals.competitors.players",
                [
                    "sport_event.id",
                    "sport_event.start_time",
                    "statistics.totals.competitors.id",
                    "statistics.totals.competitors.qualifier",
                ],
            )
            .pipe(
                lambda x: x.set_axis(
                    [remove_str("_".join(col.split(".")[-2:]), ["sport_event_", "statistics_"]) for col in x.columns],
                    axis=1,
                )
            )
        )

        return matches_statistics

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

    def get_season_competitor_player(self, season_urn: str) -> pd.DataFrame:
        """Get all players profile for a given season

        Args:
            season_urn: URN of a given season

        Returns:
            Pandas DataFrame
        """
        season_competitor_players = self.soccer_extended.get_season_competitor_players(season_urn=season_urn)
        season_competitor_players = (
            pd.json_normalize(season_competitor_players["season_competitor_players"])
            .explode("players")
            .players.apply(pd.Series)
        )

        return season_competitor_players

    def get_player_profile_info(self, player_urn: str) -> pd.DataFrame:
        """Get the basic information from a player profile

        Args:
            player_urn: URN of a given player

        Returns:
            Pandas DataFrame
        """
        player_profile = self.soccer_extended.get_player_profile(player_urn=player_urn)
        player_profile_info = pd.json_normalize(player_profile["player"])

        return player_profile_info

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
