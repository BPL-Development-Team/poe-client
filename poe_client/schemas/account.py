from datetime import datetime
from enum import Enum
from typing import Optional

from poe_client.schemas import Model


class Realm(Enum):
    """Enum to describe the different realms of an Account."""

    pc = "pc"
    xbox = "xbox"
    sony = "sony"


class Guild(Model):
    """Dataclass to describe a Guild."""

    id: int
    name: str
    tag: str
    points: Optional[int]
    status_message: Optional[str]
    created_at: datetime


class Challenge(Model):
    """Dataclass to describe a Challenge."""

    total: int


class Stream(Model):
    """Dataclass to describe the Stream data of Twitch."""

    name: str
    image: str
    status: str


class Twitch(Model):
    """Dataclass to describe a Twitch stream."""

    name: str
    stream: Optional[Stream]


class Account(Model):
    """Dataclass to describe an Account."""

    uuid: Optional[str]
    name: str
    realm: Optional[Realm]
    guild: Optional[Guild]
    challenges: Optional[Challenge]
    twitch: Optional[Twitch]
