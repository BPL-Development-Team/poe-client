from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from schemas.account import Account
from schemas.character import Character


@dataclass(frozen=True)
class LeagueRule(object):
    """Dataclass to describe a LeagueRule of a League."""

    id: str
    name: str
    description: Optional[str]


@dataclass(frozen=True)
class League(object):
    """Dataclass to describe a League."""

    id: str
    realm: Optional[str]
    description: Optional[str]
    rules: Optional[List[LeagueRule]]
    register_at: Optional[datetime]
    event: Optional[bool]
    url: Optional[str]
    start_at: Optional[datetime]
    end_at: Optional[datetime]
    timed_event: Optional[bool]
    score_event: Optional[bool]
    delve_event: Optional[bool]


@dataclass(frozen=True)
class LadderEntry(object):
    """Dataclass to describe character's LadderEntry."""

    rank: int
    dead: Optional[bool]
    retired: Optional[bool]
    online: Optional[bool]
    public: Optional[bool]
    character: Character
    account: Optional[Account]
