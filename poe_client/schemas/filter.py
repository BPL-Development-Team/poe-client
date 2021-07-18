from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class Validation(object):
    """Dataclass to describe the validation field of an ItemFilter."""

    valid: bool
    version: Optional[str]
    validated: Optional[datetime]


@dataclass(frozen=True)
class ItemFilter(object):
    """Dataclass to describe an ItemFilter."""

    id: str
    filter_name: str
    realm: str
    description: str
    version: str
    public: Optional[bool]
    filter: Optional[str]
    validation: Optional[Validation]
