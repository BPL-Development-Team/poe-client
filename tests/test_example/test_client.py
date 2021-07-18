# -*- coding: utf-8 -*-
import pytest

from poe_client.client import PoEClient
from poe_client.schemas.account import Realm
from poe_client.schemas.league import LeagueType


@pytest.mark.asyncio
async def test_list_leagues():
    """Example test with parametrization."""
    client = PoEClient("123")
    assert await client.list_leagues()
