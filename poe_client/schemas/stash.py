"""Models for stash tab changes.

THIS IS UNUSED BY THE CLIENT. These models may not actually be accurate.
"""
from enum import Enum
from typing import Dict, List, Optional, Tuple, Union

from pydantic.main import BaseConfig

from poe_client.schemas import Model


class ItemSocket(Model):
    """Dataclass to describe the ItemSocket field of an Item."""

    group: int
    attr: Optional[str]
    s_colour: Optional[str]


class ItemProperty(Model):
    """Dataclass to describe the ItemProperty field."""

    name: str
    values: List[Tuple[str, int]]  # noqa: WPS110
    display_mode: int
    progress: Optional[float]
    type: Optional[int]
    suffix: Optional[str]


class UltimatumMod(Model):
    """Dataclass to describe the UltimatumMod field of an Item."""

    type: str
    tier: int


class IncubatedItem(Model):
    """Dataclass to describe the IncubatedItem field of an Item."""

    name: str
    level: int
    progress: int
    total: int


class Hybrid(Model):
    """Dataclass to describe the Hybrid field of an Item."""

    is_vaal_gem: bool = False
    base_type_name: str
    properties: Optional[List[ItemProperty]]
    explicit_mods: Optional[List[str]]
    sec_descr_text: str


class Extended(Model):
    """Dataclass to describe the Extended field of an Item."""

    category: str
    subcategories: List[str]
    prefixed: Optional[int]
    suffixed: Optional[int]


class Colour(Enum):
    """Dataclass to describe the Colour of an Item."""

    s = "S"
    d = "D"
    i = "I"
    g = "G"


class FlavourTextParsed(Model):
    """Dataclass to describe the flavourTextParsed field."""

    id: str
    type: str
    class_: str

    class Config(BaseConfig):
        fields = {"class_": "class"}


class Scourged(Model):
    """Dataclass to describe a scourged item."""

    tier: int
    level: Optional[int]
    progress: Optional[int]
    total: Optional[int]


class Item(Model):  # noqa: WPS110
    """Dataclass to describe an Item."""

    verified: bool
    w: int
    h: int
    icon: str
    support: Optional[bool]
    stack_size: Optional[int]
    max_stack_size: Optional[int]
    stack_size_text: Optional[str]

    league: Optional[str]
    id: Optional[str]

    influences: Optional[Dict[str, str]]
    elder: Optional[bool]
    shaper: Optional[bool]
    searing: Optional[bool]
    tangled: Optional[bool]

    abyss_jewel: Optional[bool]
    delve: Optional[bool]
    fractured: Optional[bool]
    synthesised: Optional[bool]

    sockets: Optional[List[ItemSocket]]
    socketed_items: Optional[List["Item"]]

    name: str
    type_line: str
    base_type: str
    identified: bool
    item_level: Optional[bool]
    ilvl: int
    note: Optional[str]

    locked_to_character: Optional[bool]
    locked_to_account: Optional[bool]

    duplicated: Optional[bool]
    split: Optional[bool]
    corrupted: Optional[bool]

    cis_race_reward: Optional[bool]
    sea_race_reward: Optional[bool]
    th_race_reward: Optional[bool]

    properties: Optional[List[ItemProperty]]
    notable_properties: Optional[List[ItemProperty]]
    requirements: Optional[List[ItemProperty]]
    additional_properties: Optional[List[ItemProperty]]
    next_level_requirements: Optional[List[ItemProperty]]

    talisman_tier: Optional[int]
    sec_descr_text: Optional[str]

    utility_mods: Optional[List[str]]
    implicit_mods: Optional[List[str]]
    ultimatum_mods: Optional[List[UltimatumMod]]

    explicit_mods: Optional[List[str]]
    crafted_mods: Optional[List[str]]
    enchant_mods: Optional[List[str]]
    fractured_mods: Optional[List[str]]
    cosmetic_mods: Optional[List[str]]
    veiled_mods: Optional[List[str]]
    veiled: Optional[bool]

    descr_text: Optional[str]
    flavour_text: Optional[List[str]]
    flavour_text_parsed: Optional[List[Union[str, FlavourTextParsed]]]  # noqa: WPS234
    prophecy_text: Optional[str]
    is_relic: Optional[bool]
    replica: Optional[bool]

    incubated_item: Optional[IncubatedItem]
    frame_type: Optional[int]
    art_filename: Optional[str]
    hybrid: Optional[Hybrid]
    extended: Optional[Extended]

    x: Optional[int]
    y: Optional[int]
    inventory_id: Optional[str]
    socket: Optional[int]
    colour: Optional[Colour]

    # Scourge
    scourgeMods: Optional[List[str]]  # noqa: N815, WPS115
    scourged: Optional[Scourged]


class PublicStashChange(Model):
    """Dataclass to describe a PublicStashChange."""

    id: str
    public: bool
    account_name: Optional[str]
    last_character_name: Optional[str]
    stash: Optional[str]
    stash_type: str
    league: Optional[str]
    items: List[Item]  # noqa: WPS110


class PublicStash(Model):
    """Dataclass to describe a PublicStash response."""

    next_change_id: str
    stashes: List[PublicStashChange]


class Metadata(Model):
    """Dataclass to describe the Metadata of a StashTab."""

    public: Optional[bool]
    folder: Optional[bool]
    colour: Optional[str]
    items: Optional[int]  # noqa: WPS110


class StashTab(Model):
    """Dataclass to describe a StashTab."""

    id: str
    parent: Optional[str]
    name: str
    type: str
    index: Optional[int]
    metadata: Optional[Metadata]
    children: Optional[List["StashTab"]]
    items: Optional[List[Item]]  # noqa: WPS110


StashTab.update_forward_refs()
Item.update_forward_refs()
