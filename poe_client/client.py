from types import TracebackType
from typing import Callable, Dict, List, Optional, Type, TypeVar

import aiohttp
from yarl import URL

from poe_client.schemas.account import Account, Realm
from poe_client.schemas.character import Character
from poe_client.schemas.filter import ItemFilter
from poe_client.schemas.league import Ladder, League, LeagueType
from poe_client.schemas.pvp import PvPMatch, PvPMatchLadder, PvPMatchType
from poe_client.schemas.stash import PublicStash, StashTab

APIType = TypeVar("APIType")  # the variable return type


class Client(object):
    """Aiohttp class for interacting with the Path of Exile API."""

    _token: str
    _base_url: URL = URL("https://api.pathofexile.com")
    _client: aiohttp.ClientSession
    _user_agent: str

    def __init__(
        self,
        token: str,
        client_id: str,
        version: str,
        contact: str,
    ) -> None:
        """Initialize new PoE client."""
        self._token = token
        self._client = aiohttp.ClientSession(raise_for_status=True)
        self._user_agent = (
            "OAuth {clientid}/{version} (contact: {contact}) StrictMode".format(
                clientid=client_id,
                version=version,
                contact=contact,
            )
        )

    async def __aenter__(self) -> "Client":
        """Runs on entering `async with`."""
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        """Runs on exiting `async with`."""
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
        field: Optional[str] = None,
        query: Optional[Dict[str, str]] = None,
    ) -> APIType:
        """Make a get request and return a List of type APIType."""
        res = {}
        async with self._client.get(
            self._make_url(path),
            headers={
                "Authorization": "Bearer {0}".format(self._token),
                "User-Agent": self._user_agent,
            },
            raise_for_status=True,
            params=query,
        ) as resp:
            if resp.status != 200:  # noqa: WPS432
                raise ValueError()

            res = await resp.json()

        if field:
            return objtype(**res[field])

        return objtype(**res)

    async def _get_list(  # type: ignore
        self,
        path: str,
        objtype: Callable[..., APIType],
        field: str,
        query: Optional[Dict[str, str]] = None,
    ) -> List[APIType]:
        """Make a get request and return a List of type R.
        Ignores mypy type checking as we do Callable[*kwargs]"""
        res = {}
        async with self._client.get(
            self._make_url(path),
            headers={
                "Authorization": "Bearer {0}".format(self._token),
                "User-Agent": self._user_agent,
            },
            params=query,
            raise_for_status=True,
        ) as resp:
            if resp.status != 200:  # noqa: WPS432
                raise ValueError()

            res = await resp.json()

        return [objtype(**objitem) for objitem in res[field]]

    def _make_url(self, path: str) -> URL:
        return self._base_url / path


class _PvPMixin(Client):
    async def get_pvp_matches(  # noqa: WPS211
        self,
        realm: Optional[Realm] = None,
        match_type: Optional[PvPMatchType] = None,
        season: str = "",
        league: str = "",
    ) -> List[PvPMatch]:
        """Get a list of all pvp matches based on filters."""
        if match_type == PvPMatchType.season and not season:
            raise ValueError("season cannot be empty if league_type is season.")
        if match_type == PvPMatchType.league and not league:
            raise ValueError("league cannot be empty if league_type is league.")

        query = {}
        if match_type:
            query["type"] = match_type.value
        if realm:
            query["realm"] = realm.value
        if season:
            query["season"] = season
        if league:
            query["league"] = league

        return await self._get_list(
            "pvp-match",
            PvPMatch,
            "matches",
            query=query,
        )

    async def get_pvp_match(  # noqa: WPS211
        self,
        match: str,
        realm: Optional[Realm] = None,
    ) -> PvPMatch:
        """Get a pvp match based on id."""
        query = {}
        if realm:
            query["realm"] = realm.value

        return await self._get(
            "pvp-match/{0}".format(match),
            PvPMatch,
            "match",
            query=query,
        )

    async def get_pvp_match_ladder(  # noqa: WPS211
        self,
        match: str,
        realm: Optional[Realm] = None,
    ) -> PvPMatchLadder:
        """Get a pvp match based on id."""
        query = {}
        if realm:
            query["realm"] = realm.value

        return await self._get(
            "pvp-match/{0}/ladder".format(match),
            PvPMatchLadder,
            "match",
            query=query,
        )


class _LeagueMixin(Client):
    async def list_leagues(  # noqa: WPS211
        self,
        realm: Optional[Realm] = None,
        league_type: Optional[LeagueType] = None,
        offset: int = 0,
        season: str = "",
        limit: int = 50,
    ) -> List[League]:
        """Get a list of all leagues based on filters."""
        if league_type == LeagueType.season and not season:
            raise ValueError("season cannot be empty if league_type is season.")

        query = {}
        if realm:
            query["realm"] = realm.value
        if league_type:
            query["type"] = league_type.value
        if season:
            query["season"] = season
        if offset:
            query["offset"] = str(offset)
        if limit:
            query["limit"] = str(limit)

        return await self._get_list("league", League, "leagues", query=query)

    async def get_league(  # noqa: WPS211
        self,
        league: str,
        realm: Optional[Realm] = None,
    ) -> League:
        """Get a league based on league id."""
        query = {}
        if realm:
            query["realm"] = realm.value

        return await self._get(
            "league/{0}".format(league),
            League,
            "league",
            query=query,
        )

    async def get_league_ladder(  # noqa: WPS211
        self,
        league: str,
        realm: Optional[Realm] = None,
    ) -> Ladder:
        """Get the ladder of a league based on id."""
        query = {}
        if realm:
            query["realm"] = realm.value

        return await self._get(
            "league/{0}/ladder".format(league),
            Ladder,
            "ladder",
            query=query,
        )


class _AccountMixin(Client):
    async def get_profile(  # noqa: WPS211
        self,
    ) -> Account:
        """Get the account beloning to the token."""
        return await self._get("league", Account)

    async def get_characters(  # noqa: WPS211
        self,
    ) -> List[Character]:
        """Get all characters belonging to token."""
        return await self._get_list(
            "character",
            Character,
            "characters",
        )

    async def get_character(  # noqa: WPS211
        self,
        name: str,
    ) -> Character:
        """Get a character based on id and account of token."""
        return await self._get(
            "character/{0}".format(name),
            Character,
            field="character",
        )

    async def get_stashes(  # noqa: WPS211
        self,
        league: str,
    ) -> List[StashTab]:
        """Get all stash tabs belonging to token."""
        return await self._get_list(
            "stash/{0}".format(league),
            StashTab,
            "stashes",
        )

    async def get_stash(  # noqa: WPS211
        self,
        league: str,
        stash_id: str,
        substash_id: Optional[str],
    ) -> StashTab:
        """Get a stash tab based on id."""
        path = "stash/{0}/{1}".format(league, stash_id)
        if substash_id:
            path = "{0}/{1}".format(path, substash_id)

        return await self._get(
            path,
            StashTab,
            field="stash",
        )


class _FilterMixin(Client):
    async def get_item_filters(  # noqa: WPS211
        self,
    ) -> List[ItemFilter]:
        """Get all item filters."""
        return await self._get_list(
            "item-filter",
            ItemFilter,
            "filters",
        )

    async def get_item_filter(  # noqa: WPS211
        self,
        filterid: str,
    ) -> ItemFilter:
        """Get a ItemFilter based on id."""
        return await self._get(
            "item-filter/{0}".format(filterid),
            ItemFilter,
            field="filter",
        )


class _PublicStashMixin(Client):
    async def get_public_stash_tabs(  # noqa: WPS211
        self,
        page: str,
    ) -> PublicStash:
        """Get the latest public stash tabs based on page id."""
        query = {}
        if page:
            query["id"] = page

        return await self._get(
            "public-stash-tabs",
            PublicStash,
            query=query,
        )


class PoEClient(
    _PvPMixin,
    _LeagueMixin,
    _AccountMixin,
    _FilterMixin,
    _PublicStashMixin,
    Client,
):
    """Client for PoE API."""
