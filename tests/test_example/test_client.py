# -*- coding: utf-8 -*-
import asyncio
import logging
import os

import pytest
from yarl import URL

from poe_client.client import Client, PoEClient

token = os.environ.get("POE_TOKEN", "")
contact = os.environ.get("POE_CONTACT")


client = PoEClient(
    token,
    "Oauth poe-client/1.0 (contact: {contact}) StrictMode".format(contact=contact),
)


@pytest.mark.asyncio
@pytest.mark.manual
async def test_list_leagues():
    """Example test with parametrization."""
    if not token or not contact:
        raise EnvironmentError("Need to set both POE_TOKEN and POE_CONTACT")

    async with client:
        if len(client._limiter.policies) == 0:
            await client.list_leagues()

        tasks = []
        for _ in range(8):
            tasks.append(client.list_leagues())

        await asyncio.wait(tasks)


@pytest.mark.asyncio
@pytest.mark.manual
async def test_get_league():
    """Example test with parametrization."""
    if not token or not contact:
        raise EnvironmentError("Need to set both POE_TOKEN and POE_CONTACT")

    async with client:
        if len(client._limiter.policies) == 0:
            await client.get_league("Standard")

        tasks = []
        for _ in range(8):
            tasks.append(client.get_league("Standard"))

        await asyncio.wait(tasks)


@pytest.mark.asyncio
@pytest.mark.manual
async def test_get_league_ladder():
    """Example test with parametrization."""
    if not token or not contact:
        raise EnvironmentError("Need to set both POE_TOKEN and POE_CONTACT")

    async with client:
        if len(client._limiter.policies) == 0:
            await client.get_league_ladder("Standard")

        tasks = []
        for _ in range(8):
            tasks.append(client.get_league_ladder("Standard"))

        await asyncio.wait(tasks)
