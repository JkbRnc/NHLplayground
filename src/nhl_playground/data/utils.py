from nhl_playground.data.dataclasses import Play, SOG


def play2sog(play: Play) -> SOG:
    """Loads a play to SOG dataclass."""
    return SOG(
        eventId=play.eventId,
        homeTeamDefendingSide=play.homeTeamDefendingSide,
        periodDescriptor=play.periodDescriptor,
        sortOrder=play.sortOrder,
        timeInPeriod=play.timeInPeriod,
        timeRemaining=play.timeRemaining,
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
