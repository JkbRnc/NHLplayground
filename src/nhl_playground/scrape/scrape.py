import pandas as pd
from nhl_playground.scrape.scraper import NHLScraper
from typing import Any, Tuple


def fix_names(data: dict) -> dict:
    """Preprocessing function to extract names from raw data.

    Args:
        data (dict): Raw player data.

    Returns:
        dict: Raw player data with fixed names.
    """
    fixed = data.copy()
    fixed["firstName"] = data["firstName"]["default"]
    fixed["lastName"] = data["lastName"]["default"]
    return fixed


def scrape_players_team(
    scraper: NHLScraper, team: str, season: str, gt: str = "2"
) -> Tuple[list, list]:
    """Scrapes all player data from one team.

    Args:
        scraper (NHLScraper): Scraper class instance for NHL api.
        team    (str): Scraped team.
        season  (str): Scraped season.
        gt      (str, optional): game type. Defaults to "2".

    Returns:
        list, list: Skater and goalie raw data lists.
    """
    scrape_args: dict[str, str] = {"team": team, "season": season, "game_type": gt}

    raw = scraper.scrape_raw(endpoint="Team", scrape_args=scrape_args)
    skaters: list = [fix_names(d) for d in raw["skaters"]]
    goalies: list = [fix_names(d) for d in raw["goalies"]]

    return skaters, goalies


def scrape_teams_abbrev(scraper: NHLScraper) -> list[str]:
    """Scrapes team abbreviations."""
    raw_teams: list[dict] = scraper.scrape_raw(
        endpoint="TeamInfo", scrape_args={}, overwrite_base="https://api.nhle.com"
    )["data"]

    return [rt["rawTricode"] for rt in raw_teams]


def scrape_players(
    scraper: NHLScraper, season: str, gt: str = "2"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Scrapes data of all players from set season. Returns data as skater and goalie dataframes.

    Args:
        scraper (NHLScraper): Scraper class instance for NHL api.
        season  (str): Season to scrape.
        gt      (str, optional): Game type. Defaults to "2".

    Returns:
        pd.Dataframe, pd.Dataframe: Skater and goalie dataframes.
    """
    teams_abbrev: list[str] = scrape_teams_abbrev(scraper=scraper)

    skaters: list = []
    goalies: list = []

    for team in teams_abbrev:
        skaters_team, goalies_team = scrape_players_team(
            scraper=scraper, team=team, season=season, gt=gt
        )
        skaters.extend(skaters_team)
        goalies.extend(goalies_team)
    return pd.DataFrame.from_dict(skaters), pd.DataFrame.from_dict(goalies)


def scrape_ids_team_season(
    scraper: NHLScraper, team: str, season: str, gts: list[int] = [1, 2, 3]
) -> list[str]:
    """Scrapes IDs of all games in a seaso of given team"""
    games: list = scraper.scrape_raw(
        endpoint="ScheduleTeamSeason", scrape_args={"team": team, "season": season}
    )["games"]
    games = list(filter(lambda d: d["gameType"] in gts, games))
    games_ids: list = [game["id"] for game in games]

    return games_ids


def scrape_ids_season(
    scraper: NHLScraper, season: str, gts: list[int] = [1, 2, 3]
) -> list[str]:
    """Scrapes IDs of all games in a season"""
    teams_abbrev: list[str] = scrape_teams_abbrev(scraper=scraper)
    ids: list[str] = [
        id_
        for team in teams_abbrev
        for id_ in scrape_ids_team_season(
            scraper=scraper, team=team, season=season, gts=gts
        )
    ]

    return list(set(ids))


def scrape_pbp(scraper: NHLScraper, game_id: str) -> dict[str, Any]:
    """Scrapes PbP data."""
    raw_pbp: dict[str, Any] = scraper.scrape_raw(
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


def scrape_team_stats_seasons(
    scraper: NHLScraper, seasons: list[str], gts: list[int] = [1, 2, 3]
) -> list[dict[str, Any]]:
    """Scrapes all stats for given seasons"""
    teams_abbrev: list[str] = scrape_teams_abbrev(scraper)
    stats_raw = [
        scraper.scrape_raw(
            endpoint="TeamSeasonStats",
            scrape_args={"team": team, "season": season, "game-type": gt},
        )
        | {"team": team}
        for season in seasons
        for gt in gts
        for team in teams_abbrev
    ]

    stats = [
        {
            "team": d["team"],
            "season": d.get("season"),
            "gameType": d.get("gameType"),
            "skaters": [fix_names(s) for s in d.get("skaters", [])],
            "goalies": [fix_names(s) for s in d.get("goalies", [])],
        }
        for d in stats_raw
    ]
    return stats
