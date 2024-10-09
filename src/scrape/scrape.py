import pandas as pd
from scraper import NHLScraper


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
) -> (list, list):
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


def scrape_players(
    scraper: NHLScraper, season: str, gt: str = "2"
) -> (pd.DataFrame, pd.DataFrame):
    """Scrapes data of all players from set season. Returns data as skater and goalie dataframes.

    Args:
        scraper (NHLScraper): Scraper class instance for NHL api.
        season  (str): Season to scrape.
        gt      (str, optional): Game type. Defaults to "2".

    Returns:
        pd.Dataframe, pd.Dataframe: Skater and goalie dataframes.
    """
    raw_teams: list[dict] = scraper.scrape_raw(
        endpoint="TeamsStandingsNow", scrape_args={}
    )["standings"]
    teams: list[str] = [rt["teamAbbrev"]["default"] for rt in raw_teams]

    skaters: list = []
    goalies: list = []

    for team in teams:
        skaters_team, goalies_team = scrape_players_team(
            scraper=scraper, team=team, season=season, gt=gt
        )
        skaters.extend(skaters_team)
        goalies.extend(goalies_team)
    return pd.DataFrame.from_dict(skaters), pd.DataFrame.from_dict(goalies)


# scraper = NHLScraper()
# sk, gl = scrape_players(scraper=scraper, season="20232024")
# print(sk.head())
# print("Done")