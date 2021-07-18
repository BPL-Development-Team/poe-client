from datetime import datetime
from typing import Optional

from poe_client.schemas import CamelModel


class Validation(CamelModel):
    """Dataclass to describe the validation field of an ItemFilter."""

    valid: bool
    version: Optional[str]
    validated: Optional[datetime]


class ItemFilter(CamelModel):
    """Dataclass to describe an ItemFilter."""

    id: str
    filter_name: str
    realm: str
    description: str
    version: str
    public: bool = False
    filter: Optional[str]
    validation: Optional[Validation]
