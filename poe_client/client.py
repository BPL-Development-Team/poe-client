from types import TracebackType
from typing import Callable, List, Optional, Type, TypeVar

import aiohttp
from yarl import URL

from poe_client.schemas.account import Realm
from poe_client.schemas.league import Ladder, League, LeagueType

APIType = TypeVar("APIType")  # the variable return type


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

    async def _get(  # type: ignore
        self,
        path: str,
        objtype: Callable[..., APIType],
        field: str,
    ) -> APIType:
        """Make a get request and return a List of type APIType.
        Ignores mypy type checking as we do Callable[*kwargs]"""
        res = {}
        async with self._client.get(
            self._make_url(path),
            headers={"Authorization": "Bearer {0}".format(self._token)},
            raise_for_status=True,
        ) as resp:
            if resp.status != 200:  # noqa: WPS432
                raise ValueError()

            res = await resp.json()

        return objtype(**res[field])

    async def _get_list(  # type: ignore
        self,
        path: str,
        objtype: Callable[..., APIType],
        field: str,
    ) -> List[APIType]:
        """Make a get request and return a List of type R.
        Ignores mypy type checking as we do Callable[*kwargs]"""
        res = {}
        async with self._client.get(
            self._make_url(path),
            headers={"Authorization": "Bearer {0}".format(self._token)},
            raise_for_status=True,
        ) as resp:
            if resp.status != 200:  # noqa: WPS432
                raise ValueError()

            res = await resp.json()

        return [objtype(**objitem) for objitem in res[field]]

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

        return await self._get_list("league", League, "leagues")

    async def get_league(  # noqa: WPS211
        self,
        league: str,
        realm: Optional[Realm] = None,
    ) -> League:
        """Get a list of all arrays based on filters."""
        return await self._get("league/{0}".format(league), League, "league")

    async def get_league_ladder(  # noqa: WPS211
        self,
        league: str,
        realm: Optional[Realm] = None,
    ) -> Ladder:
        """Get a list of all arrays based on filters."""
        return await self._get(
            "league/{0}/ladder".format(league),
            Ladder,
            "ladder",
        )

    def _make_url(self, path: str) -> URL:
        return self._base_url / path
