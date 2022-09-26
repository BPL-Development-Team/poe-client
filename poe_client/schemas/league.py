from datetime import datetime
from enum import Enum
from typing import List, Optional

from poe_client.schemas import Model
from poe_client.schemas.account import Account
from poe_client.schemas.character import Character


class LeagueType(Enum):
    """Dataclass to describe a LeagueRule of a League."""

    main = "main"
    event = "event"
    season = "season"


class LeagueRule(Model):
    """Dataclass to describe a LeagueRule of a League."""

    id: str
    name: str
    description: Optional[str]


class League(Model):
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


class ArchnemesisProgress(Model):
    """Dataclass to describe the progress field during Archnemesis league."""

    maven_enraged_defeated: bool
    cleansing_boss_defeated: bool
    consume_boss_defeated: bool


class LadderEntry(Model):
    """Dataclass to describe character's LadderEntry."""

    rank: int
    dead: bool = False
    retired: bool = False

    # Deprecated
    online: Optional[bool] = False
    public: bool = False
    character: Character
    account: Optional[Account]
    progress: Optional[ArchnemesisProgress]


class Ladder(Model):
    """Dataclass to describe a Ladder in a league."""

    total: int
    cached_since: Optional[datetime]
    entries: List[LadderEntry]


class AtlasPassiveHashes(Model):
    """Datacass to describe the Atlas Passive field of a LeagueAccount"""

    hashes: List[int]


class LeagueAccount(Model):
    """Dataclass to describe a LeagueAccount"""

    atlas_passives: Optional[AtlasPassiveHashes]
