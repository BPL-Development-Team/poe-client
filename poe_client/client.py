import logging
from types import TracebackType
from typing import Callable, Dict, List, Optional, Type, TypeVar, Union

import aiohttp
from yarl import URL
import json

from poe_client.rate_limiter import RateLimiter
from poe_client.schemas.account import Account, Realm
from poe_client.schemas.character import Character
from poe_client.schemas.filter import ItemFilter
from poe_client.schemas.league import Ladder, League, LeagueType
from poe_client.schemas.pvp import PvPMatch, PvPMatchLadder, PvPMatchType
from poe_client.schemas.stash import PublicStash, StashTab

Model = TypeVar("Model")  # the variable return type


class Client(object):
    """Aiohttp class for interacting with the Path of Exile API."""

    _token: str
    _base_url: URL = URL("https://api.pathofexile.com")
    _client: aiohttp.ClientSession
    _user_agent: str
    _limiter: RateLimiter

    # Maps "generic" paths to rate limiting policy names.
    # Generic paths are paths with no IDs or unique numbers.
    # For example, "/character/moowiz" has an account name, so it's not a base path.
    # "/character/" is the equivalent "generic" path.
    _path_to_policy_names: Dict[str, str]

    def __init__(
        self,
        token: str,
        user_agent: str,
    ) -> None:
        """Initialize a new PoE client.

        Args:
            token: Authorization token to pass to the PoE API.
            user_agent: An OAuth user agent. Used when making HTTP requests to the API.
        """
        self._token = token
        self._user_agent = user_agent
        self._limiter = RateLimiter()
        self._path_to_policy_names = {}

    async def __aenter__(self) -> "Client":
        """Runs on entering `async with`."""
        self._client = aiohttp.ClientSession(raise_for_status=True)
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> Optional[bool]:
        """Runs on exiting `async with`."""
        await self._client.close()
        if exc_val:
            raise exc_val
        return True

    async def __get_json(
        self,
        path: str,
        path_format_args: Optional[List[str]] = None,
        query: Optional[Dict[str, str]] = None,
    ):
        """Fetches data from the POE API.

        Args:
            path: The URL path to use. Appended to the POE API base URL.
                  If certain parts of the path are non-static (account ID),
                  those should be encoded as format args ("{0}") in the path,
                  and the values for those args should be passed into
                  path_format_args.
            path_format_args: Values which should be encoded in the path when
                              the HTTP request gets made.
            query: An optional dict of query params to add to the HTTP request.

        Returns:
            The result of the API request, parsed as JSON.
        """
        if not path_format_args:
            path_format_args = []
        # We key the policy name off the path with no format args. This presumes
        # that different requests to the same endpoints with different specific
        # args use the same rate limiting. For example, /characters/moowiz
        # and /characters/chris # presumably use the same rate limiting
        # policy name.
        path_with_no_args = path.format(("" for _ in range(len(path_format_args))))
        policy_name = self._path_to_policy_names.get(path_with_no_args, "")

        kwargs: Dict[str, Optional[Union[Dict["str", "str"], bool]]] = {
            "headers": {
                "Authorization": "Bearer {0}".format(self._token),
                "User-Agent": self._user_agent,
            },
            "params": query,
        }

        semaphore = await self._limiter.get_semaphore(policy_name)

        if not semaphore:
            logging.info("BLOCKING")
            kwargs["raise_for_status"] = False
        else:
            logging.info("NOT BLOCKING")
            kwargs["raise_for_status"] = True

        url = "{0}/{1}".format(self._base_url, path.format(*path_format_args))
        # The types are ignored because for some reason it can't understand that kwargs isn't a positional
        # arg and won't override a different positional argument in the function.
        async with await self._client.get(url, **kwargs) as resp:  # type: ignore
            self._path_to_policy_names[
                path_with_no_args
            ] = await self._limiter.parse_headers(resp.headers)

            if resp.status != 200:  # noqa: WPS432
                raise ValueError(
                    "Invalid request: status code %s, expected 200" % (resp.status)
                )

            json_result = await resp.json()
            logging.debug(json_result)
            return json_result

    # Type ignore is for args and kwargs, which have unknown types we pass to __get_json
    async def _get(  # type: ignore
        self,
        model: Callable[..., Model],
        result_field: Optional[str] = None,
        *args,
        **kwargs,
    ) -> Model:
        """Make a get request and returns the data as an APIType subclass.

        Args:
            model: The object which contains data retrieved from the API. Must
                   be a sublclass of APIType.
            result_field: If present, returns the data in this field from the request,
                rather than the request itself.

        See __get_json for other args.

        Returns:
            The result, parsed into an instance of the |model| type.
        """
        json_result = await self.__get_json(*args, **kwargs)
        assert isinstance(json_result, dict)
        if result_field:
            return model(**json_result[result_field])

        return model(**json_result)

    # Type ignore is for args and kwargs, which have unknown types we pass to __get_json
    async def _get_list(  # type: ignore
        self,
        model: Callable[..., Model],
        result_field: Optional[str] = None,
        *args,
        **kwargs,
    ) -> List[Model]:
        """Make a get request and returns the data as a list of APIType subclass.

        Args:
            model: The object which contains data retrieved from the API. Must
                   be a sublclass of APIType.
            result_field: If present, returns the data in this field from the request,
                rather than the request itself.

        See __get_json for other args.

        Returns:
            The result, parsed into a list of the |model| type.
        """
        json_result = await self.__get_json(*args, **kwargs)

        if result_field:
            assert isinstance(json_result, dict)
            json_result = json_result[result_field]

        assert isinstance(json_result, list)
        return [model(**objitem) for objitem in json_result]


class _PvPMixin(Client):
    """PVP related methods for the POE API.

    CURRENTLY UNTESTED. HAS NOT BEEN USED IN PRODUCTION."""

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

        # We construct this via a dict so that the linter doesn't complain about complexity.
        query = {
            "type": match_type.value if match_type else None,
            "realm": realm.value if realm else None,
            "season": season if season else None,
            "league": league if league else None,
        }
        # Removed unset query params
        query = {key: val for key, val in query.items() if val}

        return await self._get_list(
            path="pvp-match",
            model=PvPMatch,
            result_field="matches",
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
            path="pvp-match/{0}",
            path_format_args=(match,),
            model=PvPMatch,
            result_field="match",
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
            path="pvp-match/{0}/ladder",
            path_format_args=(match,),
            model=PvPMatchLadder,
            result_field="match",
            query=query,
        )


class _LeagueMixin(Client):
    """League related methods for the POE API.

    CURRENTLY UNTESTED. HAS NOT BEEN USED IN PRODUCTION."""

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

        # We construct this via a dict so that the linter doesn't complain about complexity.
        query = {
            "realm": realm.value if realm else None,
            "type": league_type.value if league_type else None,
            "season": season if season else None,
            "offset": str(offset) if offset else None,
            "limit": str(limit) if limit else None,
        }
        # Remove unset values
        query = {key: val for key, val in query.items() if val}

        return await self._get_list(
            path="league",
            model=League,
            result_field="leagues",
            query=query,
        )

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
            path="league/{0}",
            path_format_args=(league,),
            model=League,
            result_field="league",
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
            path="league/{0}/ladder",
            path_format_args=(league,),
            model=Ladder,
            result_field="ladder",
            query=query,
        )


class _AccountMixin(Client):
    """User account methods for the POE API.

    CURRENTLY UNTESTED. HAS NOT BEEN USED IN PRODUCTION."""

    async def get_profile(  # noqa: WPS211
        self,
    ) -> Account:
        """Get the account beloning to the token."""
        return await self._get(path="league", model=Account)

    async def get_characters(  # noqa: WPS211
        self,
    ) -> List[Character]:
        """Get all characters belonging to token."""
        return await self._get_list(
            path="character",
            model=Character,
            result_field="characters",
        )

    async def get_character(  # noqa: WPS211
        self,
        name: str,
    ) -> Character:
        """Get a character based on id and account of token."""
        return await self._get(
            path="character/{0}",
            path_format_args=(name,),
            model=Character,
            result_field="character",
        )

    async def get_stashes(  # noqa: WPS211
        self,
        league: str,
    ) -> List[StashTab]:
        """Get all stash tabs belonging to token."""
        return await self._get_list(
            path="stash/{0}",
            path_format_args=(league,),
            model=StashTab,
            result_field="stashes",
        )

    async def get_stash(  # noqa: WPS211
        self,
        league: str,
        stash_id: str,
        substash_id: Optional[str],
    ) -> StashTab:
        """Get a stash tab based on id."""
        path = "stash/{0}/{1}".format(league, stash_id)
        path_format_args = [league, stash_id]
        if substash_id:
            path += "/{2}"
            path_format_args.append(substash_id)

        return await self._get(
            path=path,
            path_format_args=path_format_args,
            model=StashTab,
            result_field="stash",
        )


class _FilterMixin(Client):
    """Item Filter methods for the POE API.

    CURRENTLY UNTESTED. HAS NOT BEEN USED IN PRODUCTION."""

    async def get_item_filters(  # noqa: WPS211
        self,
    ) -> List[ItemFilter]:
        """Get all item filters."""
        return await self._get_list(
            path="item-filter",
            model=ItemFilter,
            result_field="filters",
        )

    async def get_item_filter(  # noqa: WPS211
        self,
        filterid: str,
    ) -> ItemFilter:
        """Get a ItemFilter based on id."""
        return await self._get(
            path="item-filter/{0}",
            path_format_args=(filterid,),
            model=ItemFilter,
            result_field="filter",
        )


class _PublicStashMixin(Client):
    """Public stash tab methods for the POE API.

    CURRENTLY UNTESTED. HAS NOT BEEN USED IN PRODUCTION."""

    async def get_public_stash_tabs(  # noqa: WPS211
        self,
        next_change_id: Optional[str] = None,
    ) -> PublicStash:
        """Get the latest public stash tabs.

        Args:
            next_change_id: If set, returns the next set of stash tabs, starting
                            at this change_id. While this is technically optional,
                            in practice this is required; not setting this value
                            fetches stash tabs from the beginning of the API's
                            availability which is several years in the past.

        Returns:
            An instance of the PublicStash class.
        """
        query = {}
        if next_change_id:
            query["id"] = next_change_id

        return await self._get(
            path="public-stash-tabs",
            model=PublicStash,
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
    """Client for PoE API.

    This technically has support for every API GGG has exposed. None of these
    APIs have been tested in production, so use at your own risk.
    """
