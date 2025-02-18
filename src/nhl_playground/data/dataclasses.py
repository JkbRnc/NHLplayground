from dataclasses import dataclass
from typing import Any
from numpy import ndarray


@dataclass
class SOG:
    """Shot-on-goal dataclass."""

    eventId: int
    homeTeamDefendingSide: str
    periodDescriptor: dict[str, str | int]
    sortOrder: int
    timeInPeriod: str
    timeRemaining: str
    isGoal: bool
    xCoord: int
    yCoord: int
    zoneCode: str
    shotType: str
    shootingPlayerId: int
    goalieInNetId: int
    eventOwnerTeamId: int
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
    prevDescKey: str | None = None
    prevTypeCode: str | None = None
    other: dict[str, Any] | None = None


@dataclass
class Game:
    """Game dataclass. Utilizes Play dataclass."""

    key: str
    homeTeam: dict[str, Any]
    awayTeam: dict[str, Any]
    plays: ndarray[Play]

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
        return self.plays[idx]
