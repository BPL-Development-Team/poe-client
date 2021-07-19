from enum import Enum
from typing import Dict, List, Optional, Tuple

from poe_client.schemas import CamelModel


class ItemSocket(CamelModel):
    """Dataclass to describe the ItemSocket field of an Item."""

    group: int
    attr: Optional[str]
    s_colour: Optional[str]


class ItemProperty(CamelModel):
    """Dataclass to describe the ItemProperty field."""

    name: str
    values: Tuple[str, int]  # noqa: WPS110
    display_mode: int
    progress: Optional[float]
    type: Optional[int]
    suffix: Optional[str]


class UltimatumMod(CamelModel):
    """Dataclass to describe the UltimatumMod field of an Item."""

    type: str
    tier: int


class IncubatedItem(CamelModel):
    """Dataclass to describe the IncubatedItem field of an Item."""

    name: str
    level: int
    progress: int
    total: int


class Hybrid(CamelModel):
    """Dataclass to describe the Hybrid field of an Item."""

    is_vaal_gem: bool = False
    base_type_name: str
    properties: Optional[List[ItemProperty]]
    explicit_mods: Optional[List[str]]
    sec_descr_text: str


class Extended(CamelModel):
    """Dataclass to describe the Extended field of an Item."""

    category: str
    subcategories: List[str]
    prefixed: Optional[int]
    suffixed: Optional[int]


class Colour(Enum):
    """Dataclass to describe the Colour of an Item."""

    s = "S"  # noqa: WPS111
    d = "D"  # noqa: WPS111
    i = "I"  # noqa: WPS111
    g = "G"  # noqa: WPS111


class Item(CamelModel):  # noqa: WPS110
    """Dataclass to describe an Item."""

    verified: bool
    w: int  # noqa: WPS111
    h: int  # noqa: WPS111
    icon: str
    support: Optional[bool]
    stack_size: Optional[int]
    max_stack_size: Optional[int]
    stack_size_text: Optional[str]

    league: Optional[str]
    id: Optional[str]

    influences: Dict[str, str]
    elder: Optional[bool]
    shaper: Optional[bool]
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
    ultimatum_mods: List[UltimatumMod]

    explicit_mods: Optional[List[str]]
    crafted_mods: Optional[List[str]]
    enchant_mods: Optional[List[str]]
    fractured_mods: Optional[List[str]]
    cosmetic_mods: Optional[List[str]]
    veiled_mods: Optional[List[str]]
    veiled: Optional[bool]

    descr_text: Optional[str]
    flavour_text: Optional[List[str]]
    flavour_text_parsed: Optional[List[str]]
    prophecy_text: Optional[str]
    is_relic: Optional[bool]
    replica: Optional[bool]

    incubated_item: Optional[IncubatedItem]
    frame_type: Optional[int]
    art_filename: Optional[str]
    hybrid: Optional[Hybrid]
    extended: Optional[Extended]

    x: Optional[int]  # noqa: WPS111
    y: Optional[int]  # noqa: WPS111
    inventory_id: Optional[str]
    socket: Optional[int]
    colour: Optional[Colour]


class PublicStashChange(CamelModel):
    """Dataclass to describe a PublicStashChange."""

    id: str
    public: bool
    account_name: Optional[str]
    last_character_name: Optional[str]
    stash: Optional[str]
    stash_type: str
    league: Optional[str]
    items: List[Item]  # noqa: WPS110


class PublicStash(CamelModel):
    """Dataclass to describe a PublicStash."""

    next_change_id: str
    stashes: List[PublicStashChange]


class Metadata(CamelModel):
    """Dataclass to describe the Metadata of a StashTab."""

    public: Optional[bool]
    folder: Optional[bool]
    colour: Optional[str]


class StashTab(CamelModel):
    """Dataclass to describe a StashTab."""

    id: str
    parent: Optional[str]
    name: str
    type: str
    index: Optional[int]
    metadata: Optional[Metadata]
    children: Optional[List["StashTab"]]
    items: Optional[List[Item]]  # noqa: WPS110
