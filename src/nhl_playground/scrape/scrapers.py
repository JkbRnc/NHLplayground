import logging

import requests
import yaml
from requests import Response
from nhl_playground.scrape.scrape_utils import setup_logger, remove_defaults
from typing import Any


class BaseScraper:
    """NHL scraper class using free api. Provides method for raw data scraping."""

    BASE_API_URL: str = "https://api-web.nhle.com"
    logger: logging.Logger
    ENDPOINTS: dict[str, str]

    def __init__(self, erase: bool = True) -> None:
        """Initialize scraper."""
        self._load_endpoints(path="src/nhl_playground/scrape/endpoints.yaml")
        self.logger = setup_logger("scraperLogger", "scraper.log", erase=erase)

        self.teams_abbrev = self._scrape_teams_abbrev()

    def _load_endpoints(self, path: str) -> None:
        self.ENDPOINTS = yaml.safe_load(open(path))

    def _scrape_raw(
        self,
        endpoint: str,
        scrape_args: dict[str, str],
        overwrite_base: None | str = None,
    ) -> dict[str, Any]:
        """Scrapes data from NHL api and returns unprocessed raw data.

        Args:
            endpoint (str): Endpoint name for NHL api.
            scrape_args (dict[str, str]): Arguments for formatting url.
            overwrite_base (None | str): URL to overwrite base URL. Default None.

        Returns:
            dict: Dictionary containing the raw data. Is empty when an error occures.
        """
        self.logger.info(f"Scraping of {endpoint} data started")
        base_api_url = overwrite_base if overwrite_base else self.BASE_API_URL
        try:
            response: Response = requests.get(
                f"{base_api_url}{self.ENDPOINTS[endpoint].format(**scrape_args)}"
            )
            data: dict[str, Any] = response.json()
            self.logger.info("Scraping finished succesfully")
        except Exception:
            self.logger.warning("Error occured during scraping: {e}")
            data = {}
        return data

    def _scrape_teams_abbrev(self) -> list[str]:
        """Scrapes team abbreviations."""
        raw_teams: list[dict] = self._scrape_raw(
            endpoint="TeamInfo", scrape_args={}, overwrite_base="https://api.nhle.com"
        )["data"]

        return [rt["rawTricode"] for rt in raw_teams]

    def scrape(self, season: str) -> dict[str, Any]:
        raise NotImplementedError


class TeamStatsScraper(BaseScraper):
    def scrape(self, season: str) -> dict[str, Any]:
        stats_raw = {
            team: self._scrape_raw(
                endpoint="TeamSeasonStats",
                scrape_args={"team": team, "season": season, "game-type": str(gt)},
            )
            for gt in [1, 2, 3]
            for team in self.teams_abbrev
        }
        stats: dict[str, Any] = {
            k: {
                "season": v.get("season"),
                "gameType": v.get("gameType"),
                "skaters": [remove_defaults(player) for player in v.get("skaters", [])],
                "goalies": [remove_defaults(player) for player in v.get("goalies", [])],
            }
            for k, v in stats_raw.items()
        }
        return stats


class PlayerScraper(BaseScraper):
    def scrape_players_per_team(
        self, team_abbrev: str, season: str, gts: list[int] = [1, 2, 3]
    ) -> dict[str, Any]:
        """Scrapes all player data from one team for a given season."""
        skaters: list[dict[str, Any]] = []
        goalies: list[dict[str, Any]] = []
        for gt in gts:
            scrape_args: dict[str, str] = {
                "team": team_abbrev,
                "season": season,
                "game_type": str(gt),
            }
            raw = self._scrape_raw(endpoint="Team", scrape_args=scrape_args)
            skaters.extend([remove_defaults(d) for d in raw["skaters"]])
            goalies.extend([remove_defaults(d) for d in raw["goalies"]])

        return {"skaters": skaters, "goalies": goalies}

    def scrape(self, season: str) -> dict[str, Any]:
        """Scrapes all player data from set season."""
        players: list[dict[str, Any]] = [
            self.scrape_players_per_team(team, season) for team in self.teams_abbrev
        ]
        skaters = [
            player for team_players in players for player in team_players["skaters"]
        ]
        goalies = [
            player for team_players in players for player in team_players["goalies"]
        ]

        return {"skaters": skaters, "goalies": goalies}


class PbPScraper(BaseScraper):
    def scrape_pbp_by_game_id(self, game_id: str) -> dict[str, Any]:
        raw_pbp: dict[str, Any] = self._scrape_raw(
            endpoint="PlayByPlay", scrape_args={"game-id": game_id}
        )
        raw_pbp = {
            "plays": raw_pbp["plays"],
            "homeTeam": raw_pbp["homeTeam"],
            "awayTeam": raw_pbp["awayTeam"],
        }
        raw_pbp["plays"] = [
            play | {"prevDescKey": raw_pbp["plays"][i - 1]["typeDescKey"]}
            if i > 0
            else play
            for i, play in enumerate(raw_pbp["plays"])
        ]
        return raw_pbp

    def scrape_ids_team_season(
        self, team: str, season: str, gts: list[int] = [1, 2, 3]
    ) -> list[str]:
        """Scrapes IDs of all games in a seaso of given team"""
        games: list = self._scrape_raw(
            endpoint="ScheduleTeamSeason", scrape_args={"team": team, "season": season}
        )["games"]
        games = list(filter(lambda d: d["gameType"] in gts, games))
        games_ids: list = [game["id"] for game in games]

        return games_ids

    def scrape_ids_for_season(
        self, season: str, gts: list[int] = [1, 2, 3]
    ) -> list[str]:
        """Scrapes IDs of all games in a season"""
        ids: list[str] = [
            id_
            for team in self.teams_abbrev
            for id_ in self.scrape_ids_team_season(team=team, season=season, gts=gts)
        ]

        return list(set(ids))

    def scrape(self, season: str) -> dict[str, Any]:
        """Scrapes PbP data"""
        season_ids = self.scrape_ids_for_season(season=season)
        raw_pbp = {
            game_id: self.scrape_pbp_by_game_id(game_id) for game_id in season_ids
        }
        return raw_pbp