from nhl_playground.data.dataclasses import Play, SOG


def play2sog(play: Play) -> SOG:
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
        xCoord=play.other["details"]["xCoord"],
        yCoord=play.other["details"]["yCoord"],
        zoneCode=play.other["details"]["zoneCode"],
        shotType=play.other["details"]["shotType"],
        shootingPlayerId=play.other["details"].get("shootingPlayerId")
        or play.other["details"].get("scoringPlayerId"),
        goalieInNetId=play.other["details"]["goalieInNetId"],
        eventOwnerTeamId=play.other["details"]["eventOwnerTeamId"],
    )
