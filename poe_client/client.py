from typing import List, Optional

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
        if league_type:
            if league_type.season and not season:
                raise ValueError("Season cannot be empty if league_type is season.")

        async with self._client.get(
            self._make_url("league"),
        ) as resp:
            ret = await resp.json()
            return [League(**league) for league in ret["leagues"]]

    def _make_url(self, path: str) -> URL:
        return self._base_url / path
