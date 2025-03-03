from typing import Any
from dataclasses import dataclass


@dataclass
class Enrichment:
    name: str = "Enrichment"

    def __call__(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        raise NotImplementedError


@dataclass
class AddPrevPlayName(Enrichment):
    name: str = "AddPrevPlayName"

    def __call__(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        raw_data["plays"] = [
            play
            | {
                "prevDescKey": raw_data["plays"][i - 1].get("typeDescKey"),
                "prevTypeCode": raw_data["plays"][i - 1].get("typeCode"),
            }
            if i > 0
            else play
            | {
                "prevDescKey": None,
                "prevTypeCode": -1,
            }
            for i, play in enumerate(raw_data["plays"])
        ]
        return raw_data
