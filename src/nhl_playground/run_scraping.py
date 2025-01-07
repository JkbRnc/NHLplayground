import argparse
from typing import Any
from csv import DictWriter
import json
from nhl_playground.scrape.scrapers import TeamStatsScraper, PbPScraper


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--save", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--filepath", default="", type=str)
    parser.add_argument("--parsefn", default="team_stats", type=str)
    parser.add_argument("--season", default="20222023", type=str)

    return parser


def save_csv(filename: str, data: dict[str, Any]) -> None:
    """Saves data as csv."""
    keys = data.keys()
    with open(filename, "w", newline="") as file:
        dict_writer = DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def save_json(filename: str, data: dict[str, Any]) -> None:
    """Saves data as json."""
    with open(filename, "w") as outfile:
        json.dump(data, outfile)


def main(args: Any) -> None:
    print(f"Starting to parse {args.parsefn}")

    scrapers_mapping = {"team_stats": TeamStatsScraper, "pbp": PbPScraper}
    scraper = scrapers_mapping.get(args.parsefn)
    if scraper:
        scraper = scraper()
        stats = scraper.scrape(season=args.season)
    else:
        stats = {}

    if args.save:
        # save_csv(args.filepath, stats)
        save_json(args.filepath, stats)
    else:
        print(len(stats.keys()))


if __name__ == "__main__":
    parser = setup_parser()
    main(parser.parse_args())
