from dataclasses import dataclass
from typing import Any


@dataclass
class Enrichment:
    """Base enrichment class."""

    name: str = "Enrichment"

    def __call__(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Abstract method to be implemented by subclasses."""
        raise NotImplementedError


@dataclass
class AddPrevPlayName(Enrichment):
    """Simple enrichment that adds previous play name and type code to each play."""

    name: str = "AddPrevPlayName"

    def __call__(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Adds previous play name and type code to each play."""
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
