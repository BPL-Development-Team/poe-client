from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from schemas.account import Account
from schemas.character import Character


@dataclass(frozen=True)
class PvPLadderTeamMember(object):
    """Dataclass to describe a member of a PvPLadderTeamEntry."""

    account: Account
    character: Character
    public: Optional[bool]


@dataclass(frozen=True)
class PvPLadderTeamEntry(object):
    """Dataclass to describe a PvPLadderTeamEntry."""

    rank: int
    rating: Optional[int]
    points: Optional[int]
    games_played: Optional[int]
    cumulative_opponent_points: Optional[int]
    last_game_time: Optional[datetime]
    members: List[PvPLadderTeamMember]
