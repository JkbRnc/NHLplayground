from nhl_playground.data.dataclasses import Play, SOG


def time2sec(time_str: str) -> int:
    time = tuple(int(t) for t in time_str.split(":"))
    return 60 * time[0] + time[1]


def play2sog(play: Play) -> SOG:
    """Loads a play to SOG dataclass."""
    return SOG(
        eventId=play.eventId,
        homeTeamDefendingSide=play.homeTeamDefendingSide,
        periodNumber=play.periodDescriptor["number"],
        periodType=play.periodDescriptor["periodType"],
        sortOrder=play.sortOrder,
        timeInPeriod=time2sec(play.timeInPeriod),
        timeRemaining=time2sec(play.timeRemaining),
        prevDescKey=play.prevDescKey,
        prevTypeCode=play.prevTypeCode,
        isGoal=play.typeDescKey == "goal",
        xCoord=play.other["details"].get("xCoord"),  # TODO impute missing values
        yCoord=play.other["details"].get("yCoord"),  #
        zoneCode=play.other["details"].get("zoneCode"),  #
        shotType=play.other["details"].get("shotType"),  #
        shootingPlayerId=play.other["details"].get("shootingPlayerId")
        or play.other["details"].get("scoringPlayerId"),
        goalieInNetId=play.other["details"].get("goalieInNetId"),
        eventOwnerTeamId=play.other["details"]["eventOwnerTeamId"],
    )
