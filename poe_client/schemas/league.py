from datetime import datetime
from enum import Enum
from typing import List, Optional

from poe_client.schemas import CamelModel
from poe_client.schemas.account import Account
from poe_client.schemas.character import Character


class LeagueType(Enum):
    """Dataclass to describe a LeagueRule of a League."""

    main = "main"
    event = "event"
    season = "season"


class LeagueRule(CamelModel):
    """Dataclass to describe a LeagueRule of a League."""

    id: str
    name: str
    description: Optional[str]


class League(CamelModel):
    """Dataclass to describe a League."""

    id: str
    realm: Optional[str]
    description: Optional[str]
    rules: Optional[List[LeagueRule]]
    register_at: Optional[datetime]
    event: bool = False
    url: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    timed_event: bool = False
    score_event: bool = False
    delve_event: bool = False


class LadderEntry(CamelModel):
    """Dataclass to describe character's LadderEntry."""

    rank: int
    dead: bool = False
    retired: bool = False
    online: bool = False
    public: bool = False
    character: Character
    account: Optional[Account]


class Ladder(CamelModel):
    total: int
    cached_since: Optional[datetime]
    entries: List[LadderEntry]
