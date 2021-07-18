from types import TracebackType
from typing import List, Optional, Type

import aiohttp
from yarl import URL

from poe_client.schemas.account import Realm
from poe_client.schemas.league import League, LeagueType


class PoEClient(object):
    """Aiohttp class for interacting with the Path of Exile API."""

    _token: str
    _base_url: URL = URL("https://api.pathofexile.com")
    _client: aiohttp.ClientSession

    def __init__(
        self,
        token: str,
    ) -> None:
        """Initialize new PoE client."""
        self._token = token
        self._client = aiohttp.ClientSession(raise_for_status=True)

    async def __aenter__(self) -> "PoEClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        await self.close()
        if exc_val:
            raise exc_val
        return True

    async def close(self) -> None:
        """Close client connection."""
        return await self._client.close()

    async def list_leagues(  # noqa: WPS211
        self,
        realm: Optional[Realm] = None,
        league_type: Optional[LeagueType] = None,
        offset: int = 0,
        season: str = "",
        limit: int = 50,
    ) -> List[League]:
        """Get a list of all arrays based on filters."""
        if league_type == LeagueType.season and not season:
            raise ValueError("season cannot be empty if league_type is season.")

        res = {}
        async with self._client.get(
            self._make_url("league"),
            headers={"Authorization": "Bearer {0}".format(self._token)},
            raise_for_status=True,
        ) as resp:
            if resp.status != 200:  # noqa: WPS432
                raise ValueError()

            res = await resp.json()

        leagues: List[League] = [League.parse_obj(league) for league in res["leagues"]]

        return leagues

    def _make_url(self, path: str) -> URL:
        return self._base_url / path
