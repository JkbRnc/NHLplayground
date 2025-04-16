from nhl_playground.data.dataclasses import SOG, Play


def time2sec(time_str: str) -> int:
    """Transforms time string to seconds."""
    time = tuple(int(t) for t in time_str.split(":"))
    return 60 * time[0] + time[1]


def play2sog(play: Play) -> SOG:
    """Loads a play to SOG dataclass."""
    assert play.typeDescKey in ["shot-on-goal", "goal"], "Play is not a shot-on-goal or goal"
    return SOG(
        eventId=play.eventId,
        homeTeamDefendingSide=play.homeTeamDefendingSide,
        periodNumber=int(play.periodDescriptor["number"]),
        periodType=str(play.periodDescriptor["periodType"]),
        sortOrder=play.sortOrder,
        timeInPeriod=time2sec(play.timeInPeriod),
        timeRemaining=time2sec(play.timeRemaining),
        prevDescKey=play.prevDescKey,
        prevTypeCode=play.prevTypeCode,
        isGoal=play.typeDescKey == "goal",
        xCoord=play.other["details"].get("xCoord"),  # TODO impute missing values
        yCoord=play.other["details"].get("yCoord"),  #
        zoneCode=str(play.other["details"].get("zoneCode")),  #
        shotType=str(play.other["details"].get("shotType")),  #
        shootingPlayerId=play.other["details"].get("shootingPlayerId") or play.other["details"].get("scoringPlayerId"),
        goalieInNetId=play.other["details"].get("goalieInNetId", -1),
        eventOwnerTeamId=play.other["details"]["eventOwnerTeamId"],
        situationCode=int(play.other["situationCode"]),
    )
