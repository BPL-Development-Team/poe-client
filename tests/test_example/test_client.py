# -*- coding: utf-8 -*-
import logging

import pytest
from yarl import URL

from poe_client.client import Client, PoEClient


@pytest.mark.asyncio()
async def test_make_url():
    """Test that make_url makes a correct path."""
    client = Client("")
    assert client._make_url("path") == URL(  # noqa: WPS437
        "{0}/{1}".format(
            client._base_url,  # noqa: WPS437
            "path",
        ),
    )
    await client.close()


@pytest.mark.asyncio()
@pytest.mark.integtest()
async def test_list_leagues():
    """Example test with parametrization."""
    client = PoEClient("")
    leagues = []
    async with client:
        leagues = await client.list_leagues()
        logging.info(leagues)

    assert leagues


@pytest.mark.asyncio()
@pytest.mark.integtest()
async def test_get_league():
    """Example test with parametrization."""
    client = PoEClient("")
    async with client:
        league = await client.get_league("Ultimatum")

    assert league


@pytest.mark.asyncio()
@pytest.mark.integtest()
async def test_get_league_ladder():
    """Example test with parametrization."""
    client = PoEClient("")
    async with client:
        league = await client.get_league_ladder("Ultimatum")

    assert league


"""
@pytest.mark.asyncio()
async def test_get_pvp_matches():
    """ "Example test with parametrization." """
    client = PoEClient("")
    async with client:
        league = await client.get_pvp_matches()

    assert league
"""
