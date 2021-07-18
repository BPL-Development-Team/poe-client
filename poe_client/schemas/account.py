from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class Realm(Enum):
    """Enum to describe the different realms of an Account."""

    pc = "pc"
    xbox = "xbox"
    sony = "sony"


@dataclass(frozen=True)
class Guild(object):
    """Dataclass to describe a Guild."""

    id: int
    name: str
    tag: str
    points: Optional[int]
    status_message: Optional[str]
    created_at: datetime


@dataclass(frozen=True)
class Challenge(object):
    """Dataclass to describe a Challenge."""

    total: int


@dataclass(frozen=True)
class Stream(object):
    """Dataclass to describe the Stream data of Twitch."""

    name: str
    image: str
    status: str


@dataclass(frozen=True)
class Twitch(object):
    """Dataclass to describe a Twitch stream."""

    name: str
    stream: Optional[Stream]


@dataclass(frozen=True)
class Account(object):
    """Dataclass to describe an Account."""

    name: str
    realm: Optional[Realm]
    guild: Optional[Guild]
    challenges: Optional[Challenge]
    twitch: Optional[Twitch]
