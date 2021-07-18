# -*- coding: utf-8 -*-
import logging

import pytest

from poe_client.client import PoEClient


@pytest.mark.asyncio
async def test_list_leagues():
    """Example test with parametrization."""

    client = PoEClient("")
    leagues = []
    async with client:
        leagues = await client.list_leagues()

    assert leagues
