from dataclasses import dataclass
from typing import Any

from numpy import ndarray


@dataclass
class SOG:
    """Shot-on-goal dataclass."""

    eventId: int
    homeTeamDefendingSide: str
    periodNumber: int
    periodType: str
    sortOrder: int
    timeInPeriod: int
    timeRemaining: int
    isGoal: bool
    xCoord: int | None
    yCoord: int | None
    zoneCode: str | None
    shotType: str | None
    shootingPlayerId: int | None
    goalieInNetId: int | None
    eventOwnerTeamId: int
    situationCode: int

    # Values add by enrichments
    prevDescKey: str | None = None
    prevTypeCode: int | None = None


@dataclass
class Play:
    """Play dataclass."""

    eventId: int
    homeTeamDefendingSide: str
    periodDescriptor: dict[str, str | int]
    sortOrder: int
    timeInPeriod: str
    timeRemaining: str
    typeCode: int
    typeDescKey: str
    other: dict[str, Any]

    # Values added by enrichments
    prevDescKey: str | None = None
    prevTypeCode: int | None = None


@dataclass
class Game:
    """Game dataclass. Utilizes Play dataclass."""

    key: str
    homeTeam: dict[str, int]
    awayTeam: dict[str, int]
    plays: ndarray

    @property
    def homeTeam_id(self) -> int:
        """Gets home team ID."""
        return self.homeTeam["id"]

    @property
    def awayTeam_id(self) -> int:
        """Gets away team ID."""
        return self.awayTeam["id"]

    def __getitem__(self, idx: int) -> Play | None:
        """Gets play on a given index."""
        if abs(idx) > len(self.plays):
            return None
        return self.plays[idx]  # type: ignore[no-any-return]
