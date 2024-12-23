import argparse
from typing import Any
from csv import DictWriter
from nhl_playground.scrape.scraper import NHLScraper
from nhl_playground.scrape.scrape import scrape_team_stats_seasons


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument("--save", default=False, action=argparse.BooleanOptionalAction)
    parser.add_argument("--filepath", default="", type=str)
    parser.add_argument("--parsefn", default="team_stats", type=str)

    return parser


def save_csv(filename: str, data: list[dict[str, Any]]):
    keys = data[0].keys()
    with open(filename, "w", newline="") as file:
        dict_writer = DictWriter(file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)


def main(args):
    scraper = NHLScraper()
    match args.parsefn:
        case "team_stats":
            print(f"Starting to parse {args.parsefn}")
            stats = scrape_team_stats_seasons(
                scraper=scraper, seasons=["20222023", "20212022"]
            )
        case "pbp":
            stats = []
        case _:
            stats = []

    if args.save:
        save_csv(args.filepath, stats)
    else:
        len(stats)


if __name__ == "__main__":
    parser = setup_parser()
    main(parser.parse_args())
