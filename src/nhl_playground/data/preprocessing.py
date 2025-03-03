from abc import ABC, abstractclassmethod
from typing import Any, TypeVar

from numpy import append, array, frompyfunc
from pandas import DataFrame

from nhl_playground.data.dataclasses import Game, Play
from nhl_playground.data.dataloaders import BaseLoader
from nhl_playground.data.enrichment import AddPrevPlayName, Enrichment
from nhl_playground.data.utils import play2sog

T = TypeVar("T")


class BasePreprocessor(ABC):
    """Base class for preprocessors."""

    def __init__(self, loader: BaseLoader | None = None) -> None:
        """Base constructor."""
        self.enrichments = array([])
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
                self.enrichments = append(self.enrichments, e())
            else:
                raise ValueError("Invalid enrichment name.")
        else:
            self.enrichments = append(self.enrichments, enrichment())

    def apply_enrichments(self, raw_data: dict[str, Any]) -> dict[str, Any]:
        """Applies a sequence of added enrichments to input data."""
        res = raw_data
        for fn in self.enrichments:
            res = fn(raw_data)
        return res

    @abstractclassmethod
    def format(self, obj: T) -> DataFrame:
        """Formats input object into pd.DataFrame."""
        pass


class XGPreprocessor(BasePreprocessor):
    """Preprocessor for xG models."""

    def __init__(self) -> None:
        super().__init__(self)
        pass

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
        self.loader.load(enriched_raw)

        enriched_games = [
            play2sog(play)
            for game in self.loader
            for play in self._filter_shots(game).plays
        ]

        return DataFrame(enriched_games)


# (
#     {
#         "eventId": 381,
#         "periodDescriptor": {
#             "number": 1,
#             "periodType": "REG",
#             "maxRegulationPeriods": 3,
#         },
#         "timeInPeriod": "18:02",
#         "timeRemaining": "01:58",
#         "situationCode": "1551",
#         "homeTeamDefendingSide": "left",
#         "typeCode": 505,
#         "typeDescKey": "goal",
#         "sortOrder": 222,
#         "details": {
#             "xCoord": 30,
#             "yCoord": 7,
#             "zoneCode": "O",
#             "shotType": "slap",
#             "scoringPlayerId": 8480035,
#             "scoringPlayerTotal": 2,
#             "assist1PlayerId": 8482671,
#             "assist1PlayerTotal": 7,
#             "eventOwnerTeamId": 7,
#             "goalieInNetId": 8479406,
#             "awayScore": 0,
#             "homeScore": 1,
#             "highlightClipSharingUrl": "https://nhl.com/video/min-buf-jokiharju-scores-goal-against-wild-6340906550112",
#             "highlightClip": 6340906550112,
#         },
#         "pptReplayUrl": "https://wsr.nhle.com/sprites/20232024/2023020204/ev381.json",
#     },
# )
