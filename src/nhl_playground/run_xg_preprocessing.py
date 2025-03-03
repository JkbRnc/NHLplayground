from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from time import time

from numpy import sum
from pandas import DataFrame, isna

from nhl_playground.data.dataloaders import PbPDataLoader
from nhl_playground.data.preprocessing import XGPreprocessor


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
    start = time()
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

    end = time()
    # Save data as csv or prints first 10 rows
    if variables.save:
        data.to_csv(path_or_buf=variables.outfile, sep=";")
        print(f"Data saved to {variables.outfile}")
    else:
        print(data.head())
        output = [
            [
                col,
                len(data) - sum(isna(data[col])),
                data[col].nunique(),
                str(data[col].dtype),
            ]
            for col in data.columns
        ]
        print(
            DataFrame(
                output, columns=["name", "non-null", "unique", "dtype"]
            ).set_index("name")
        )
    print(f"Elapsed time: {end - start}s")


if __name__ == "__main__":
    parser = setup_parser()
    args = parser.parse_args()
    variables = InputVariables(
        save=args.save,
        infile=args.input,
        outfile=args.output,
        enrichment=args.enrichment or [],
    )
    main(variables)
