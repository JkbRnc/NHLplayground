from __future__ import annotations
import argparse
import json
from nhl_playground.data.dataloaders import PbPDataLoader
from nhl_playground.data.preprocessing import XGPreprocessor
from pandas import DataFrame
from dataclasses import dataclass


@dataclass
class InputVariables:
    save: bool
    outfile: str
    infile: str
    enrichment: list[str]


def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-s",
        "--save",
        default=False,
        action=argparse.BooleanOptionalAction,
        help="Save flag, defaults to false.",
    )
    parser.add_argument(
        "-o", "--output", default="", type=str, help="Output file path."
    )
    parser.add_argument(
        "-i", "--input", default="data/pbp_raw.json", type=str, help="Input file path."
    )
    parser.add_argument(
        "-e",
        "--enrichment",
        action="append",
        type=str,
        help="Enrichment function name.",
    )

    return parser


def main(variables: InputVariables) -> None:
    """
    This script runs preprocessing for xG models. It requires path
    to JSON data in a following format:

    {
        "game_key" : <game_json>
    }

    Enrichments can be passed as arguments with '-e' switch.
    For all possible enrichment keyword options check README.
    """
    # Set up preprocessor
    preprocessor = XGPreprocessor()
    preprocessor.loader = PbPDataLoader()

    for e in variables.enrichment:
        try:
            preprocessor.add_enrichment(e)
        except ValueError as ve:
            print("Error occured when adding enrichment: ", ve)

    # Load raw data to loader within preprocessor
    with open(variables.infile) as input_file:
        raw_data = json.load(input_file)
    data: DataFrame = preprocessor.format(raw_data)

    # Save data as csv or prints first 10 rows
    if variables.save:
        data.to_csv(path_or_buf=variables.outfile, sep=";")
    else:
        print(data.head())


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    variables = InputVariables(
        save=args.save,
        infile=args.input,
        outfile=args.output,
        enrichment=args.enrichment,
    )
    main(variables)
