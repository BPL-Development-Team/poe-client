from typing import Dict, List, Optional

from pydantic import BaseConfig

from poe_client.schemas import CamelModel
from poe_client.schemas.account import Account
from poe_client.schemas.stash import Item


class Depth(CamelModel):
    """Dataclass to describe the Delve data of a Character."""

    default: Optional[int]
    solo: Optional[int]


class Group(CamelModel):
    """Dataclass to describe the Group field of a Subgraph."""

    proxy: str
    nodes: List[str]
    x: float  # noqa: WPS111
    y: float  # noqa: WPS111
    orbits: List[int]


class Node(CamelModel):
    """Dataclass to describe the Node field of a Subgraph."""

    skill: str
    name: str
    icon: str
    stats: List[str]
    is_mastery: bool = False
    group: str
    orbit: int
    orbit_index: int
    out: List[str]
    in_: List[str]


class Subgraph(CamelModel):
    """Dataclass to describe the Subgraph field of Passives."""

    groups: Dict[str, Group]
    nodes: Dict[str, Node]


class ItemJewelData(CamelModel):
    """Dataclass to describe jewel_data in Passives."""

    type: str
    radius: Optional[int]
    radius_min: Optional[int]
    radius_visual: Optional[str]
    subgraph: Optional[Subgraph]


class Passives(CamelModel):
    """Dataclass to describe the passive tree of a character."""

    hashes: List[int]
    hashes_ex: List[int]
    bandit_choice: Optional[str]
    pantheon_major: Optional[str]
    pantheon_minor: Optional[str]
    jewel_data: Dict[int, ItemJewelData]


class Character(CamelModel):
    """Dataclass to describe a Character."""

    id: str
    name: str
    class_: str
    league: Optional[str]
    level: int
    experience: Optional[int]
    expired: bool = False
    deleted: bool = False
    current: bool = False
    equipment: Optional[List[Item]]
    inventory: Optional[List[Item]]
    jewels: Optional[List[Item]]
    time: Optional[int]
    score: Optional[int]
    depth: Optional[Depth]
    account: Optional[Account]
    passives: Optional[Passives]

    class Config(BaseConfig):
        fields = {"class_": "class"}
