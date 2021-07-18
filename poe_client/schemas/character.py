from dataclasses import dataclass
from typing import Dict, List, Optional

from schemas.account import Account
from schemas.stash import Item


@dataclass(frozen=True)
class Depth(object):
    """Dataclass to describe the Delve data of a Character."""

    default: Optional[int]
    solo: Optional[int]


@dataclass(frozen=True)
class Group(object):
    """Dataclass to describe the Group field of a Subgraph."""

    proxy: str
    nodes: List[str]
    x: float  # noqa: WPS111
    y: float  # noqa: WPS111
    orbits: List[int]


@dataclass(frozen=True)
class Node(object):
    """Dataclass to describe the Node field of a Subgraph."""

    skill: str
    name: str
    icon: str
    stats: List[str]
    is_mastery: Optional[bool]
    group: str
    orbit: int
    orbit_index: int
    out: List[str]
    in_: List[str]


@dataclass(frozen=True)
class Subgraph(object):
    """Dataclass to describe the Subgraph field of Passives."""

    groups: Dict[str, Group]
    nodes: Dict[str, Node]


@dataclass(frozen=True)
class ItemJewelData(object):
    """Dataclass to describe jewel_data in Passives."""

    type: str
    radius: Optional[int]
    radius_min: Optional[int]
    radius_visual: Optional[str]
    subgraph: Optional[Subgraph]


@dataclass(frozen=True)
class Passives(object):
    """Dataclass to describe the passive tree of a character."""

    hashes: List[int]
    hashes_ex: List[int]
    bandit_choice: Optional[str]
    pantheon_major: Optional[str]
    pantheon_minor: Optional[str]
    jewel_data: Dict[int, ItemJewelData]


@dataclass(frozen=True)
class Character(object):
    """Dataclass to describe a Character."""

    id: str
    name: str
    class_: str
    league: Optional[str]
    level: int
    experience: Optional[int]
    expired: Optional[bool]
    deleted: Optional[bool]
    current: Optional[bool]
    equipment: Optional[List[Item]]
    inventory: Optional[List[Item]]
    jewels: Optional[List[Item]]
    time: Optional[int]
    score: Optional[int]
    depth: Optional[Depth]
    account: Optional[Account]
    passives: Optional[Passives]
