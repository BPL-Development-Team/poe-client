from datetime import datetime
from enum import Enum
from typing import List, Optional

from poe_client.schemas import Model
from poe_client.schemas.account import Account
from poe_client.schemas.character import Character


class PvPMatchType(Enum):
    """Dataclass to describe a LeagueRule of a League."""

    upcoming = "upcoming"
    season = "season"
    league = "league"


class PvPStyle(Enum):
    """Dataclass to describe the Style of a PvP Match."""

    blitz = "blitz"
    swiss = "swiss"
    arena = "arena"


class PvPLadderTeamMember(Model):
    """Dataclass to describe a member of a PvPLadderTeamEntry."""

    account: Account
    character: Character
    public: bool = False


class PvPLadderTeamEntry(Model):
    """Dataclass to describe a PvPLadderTeamEntry."""

    rank: int
    rating: Optional[int]
    points: Optional[int]
    games_played: Optional[int]
    cumulative_opponent_points: Optional[int]
    last_game_time: Optional[datetime]
    members: List[PvPLadderTeamMember]


class PvPMatch(Model):
    """Dataclass to describe PvPMatch."""

    id: str
    realm: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    url: Optional[str]
    description: str
    glicko_ratings: bool
    pvp: bool = True
    style: PvPStyle
    register_at: Optional[str]
    complete: bool = False
    upcoming: bool = False
    in_progress: bool = False


class PvPLadder(Model):
    """Dataclass to describe PvPLadder."""

    total: int
    entries: List[PvPLadderTeamEntry]


class PvPMatchLadder(Model):
    """Dataclass to describe PvPMatchLadder."""

    match: PvPMatch
    ladder: PvPLadder
