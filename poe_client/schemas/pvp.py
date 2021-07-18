from datetime import datetime
from typing import List, Optional

from poe_client.schemas import CamelModel
from poe_client.schemas.account import Account
from poe_client.schemas.character import Character


class PvPLadderTeamMember(CamelModel):
    """Dataclass to describe a member of a PvPLadderTeamEntry."""

    account: Account
    character: Character
    public: bool = False


class PvPLadderTeamEntry(CamelModel):
    """Dataclass to describe a PvPLadderTeamEntry."""

    rank: int
    rating: Optional[int]
    points: Optional[int]
    games_played: Optional[int]
    cumulative_opponent_points: Optional[int]
    last_game_time: Optional[datetime]
    members: List[PvPLadderTeamMember]
