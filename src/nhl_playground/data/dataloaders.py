from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any

from numpy import array, concatenate, ndarray

from nhl_playground.data.dataclasses import Game, Play


class GameLoader:
    """Loader class for loading games into Game dataclasses."""

    @classmethod
    def load_game(cls, raw_game: dict[str, Any]) -> Game:
        """Loads game into Game dataclass."""
        plays = array([cls.load_play(play) for play in raw_game["plays"]])
        return Game(
            key=raw_game["key"],
            homeTeam=raw_game["homeTeam"],
            awayTeam=raw_game["awayTeam"],
            plays=plays,
        )

    @classmethod
    def load_play(
        cls,
        raw_play: dict[str, Any],
        mutual_keys: tuple[str, ...] = (
            "eventId",
            "homeTeamDefendingSide",
            "periodDescriptor",
            "sortOrder",
            "timeInPeriod",
            "timeRemaining",
            "typeCode",
            "typeDescKey",
            "prevDescKey",
            "prevTypeCode",
        ),
    ) -> Play:
        """Loads play into Play dataclass."""
        other_keys = {k for k in raw_play if k not in mutual_keys}

        mutual_data: dict[str, Any] = {k: raw_play.get(k) for k in mutual_keys}
        other: dict[str, Any] = {k: raw_play.get(k) for k in other_keys}
        return Play(other=other, **mutual_data)


class BaseLoader(ABC, Iterator):
    """Base class for data loaders."""

    @abstractmethod
    def next(self) -> object:
        """Returns next element in the iterator."""
        raise NotImplementedError

    @abstractmethod
    def load(self, raw_data: dict[str, Any]) -> None:
        """Abstract method for loaders."""
        raise NotImplementedError


class PbPDataLoader(BaseLoader):
    """Play-by-play data loader."""

    def __init__(self) -> None:
        """PbP loader constructor."""
        self.games: ndarray = array([])

    def __getitem__(self, idx: int) -> Game | None:
        """Gets game based on index."""
        if abs(idx) > len(self.games):
            return None
        return self.games[idx]  # type: ignore[no-any-return]

    def __len__(self) -> int:
        """Length attribute."""
        return len(self.games)

    def load(self, raw_games: dict[str, Any]) -> None:
        """Loads games from dictionary."""
        raw_games_list = [game | {"key": key} for key, game in array(list(raw_games.items()))]
        games = array([GameLoader.load_game(raw_game) for raw_game in raw_games_list])

        self.games = concatenate((self.games, games))
