from abc import ABC, abstractmethod
from typing import Any

from numpy import frompyfunc
from pandas import DataFrame

from nhl_playground.data.dataclasses import Game, Play
from nhl_playground.data.dataloaders import BaseLoader
from nhl_playground.data.enrichment import AddPrevPlayName, Enrichment
from nhl_playground.data.utils import play2sog


class BasePreprocessor(ABC):
    """Base class for preprocessors."""

    def __init__(self, loader: BaseLoader | None = None) -> None:
        """Base constructor."""
        self.enrichments: list[Enrichment] = []
        self._loader = loader

    @property
    def loader(self) -> BaseLoader | None:
        """Loader property."""
        return self._loader

    @loader.setter
    def loader(self, loader: BaseLoader) -> None:
        """Loader setter."""
        self._loader = loader

    def add_enrichment(self, enrichment: Enrichment | str) -> None:
        """Appends enrichment to the sequence."""
        if isinstance(enrichment, str):
            enrichment_mapping = {"add_prev_play_name": AddPrevPlayName}
            if e := enrichment_mapping.get(enrichment):
                self.enrichments.append(e())
            else:
                raise ValueError("Invalid enrichment name.")
        else:
            self.enrichments.append(enrichment)

    def apply_enrichments(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Applies a sequence of added enrichments to input data."""
        res = raw_data
        for fn in self.enrichments:
            res = fn(raw_data)
        return res

    @abstractmethod
    def format(self, raw: dict[str, Any]) -> DataFrame:
        """Formats input object into pd.DataFrame."""


class XGPreprocessor(BasePreprocessor):
    """Preprocessor for xG models."""

    def __init__(self) -> None:
        """XG Preprocessor constructor."""
        super().__init__()

    @staticmethod
    def _is_shot(play: Play) -> bool:
        """Checks if the play was SOG or a goal."""
        return play.typeDescKey in ["shot-on-goal", "goal"]

    def _filter_shots(self, game: Game) -> Game:
        """Filters out all plays except shots on goal and goals."""
        filter_shots = frompyfunc(XGPreprocessor._is_shot, 1, 1)
        shot_idxs = filter_shots(game.plays)
        game.plays = game.plays[shot_idxs.tolist()]

        return game

    def format(self, raw: dict[str, Any]) -> DataFrame:
        """Formats raw data to Pandas DataFrame while applying all enrichments and SOG filtering."""
        enriched_raw = {key: self.apply_enrichments(game) for key, game in raw.items()}
        assert self.loader is not None, "Loader must be set before loading data."
        self.loader.load(enriched_raw)

        enriched_games = [play2sog(play) for game in self.loader for play in self._filter_shots(game).plays]

        return DataFrame(enriched_games)
