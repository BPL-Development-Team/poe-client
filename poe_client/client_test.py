from unittest import IsolatedAsyncioTestCase, mock

import pytest
from yarl import URL

from poe_client import client
from poe_client.schemas import Model
from poe_client.schemas.stash import PublicStash


class ModelTest(Model):
    """Test Model."""

    thing: str


class ClientTest(IsolatedAsyncioTestCase):
    """Tests the POE client.

    Several lines have typing ignored because we're mocking out elements of
    the class for testing, which the typing system doesn't understand.
    """

    def setUp(self) -> None:
        """Sets up the test."""
        self.client = client.PoEClient("token", "test user agent")
        self.client._base_url = URL("https://example.com")
        self.client._client = mock.AsyncMock()
        return super().setUp()

    async def test_complete(self):
        """Complete test of the client (asserts on most observable outputs)."""
        response_mock = mock.MagicMock()
        response_mock.status = 200
        response_mock.headers = {}
        response_mock.json = mock.AsyncMock(return_value={"model": {"thing": "1"}})
        self.client._client.get.return_value.__aenter__.return_value = (  # type: ignore
            response_mock
        )

        get_result = await self.client._get(
            model=ModelTest,
            result_field="model",
            path="test",
        )
        assert get_result == ModelTest(thing="1")
        self.client._client.get.assert_called_with(
            "https://example.com/test",
            headers={
                "Authorization": "Bearer token",
                "User-Agent": "test user agent",
            },
            params=None,
            raise_for_status=False,
        )

    async def test_no_result_field(self):
        """Tests not passing a result field argument."""
        response_mock = mock.MagicMock()
        response_mock.status = 200
        response_mock.headers = {}
        response_mock.json = mock.AsyncMock(return_value={"thing": "123"})
        self.client._client.get.return_value.__aenter__.return_value = (  # type: ignore
            response_mock
        )

        get_result = await self.client._get(
            model=ModelTest,
            path="test",
        )
        assert get_result == ModelTest(thing="123")

    async def test_get_list(self):
        """Tests the get_list method."""
        response_mock = mock.MagicMock()
        response_mock.status = 200
        response_mock.headers = {}
        response_mock.json = mock.AsyncMock(
            return_value={
                "model": [
                    {"thing": "12"},
                    {"thing": "98"},
                ]
            }
        )
        self.client._client.get.return_value.__aenter__.return_value = (  # type: ignore
            response_mock
        )

        get_list_result = await self.client._get_list(
            model=ModelTest,
            result_field="model",
            path="test",
        )
        assert get_list_result == [ModelTest(thing="12"), ModelTest(thing="98")]

    async def test_wrong_status(self):
        """Tests that the client throws an exception with an invalid HTTP status."""
        response_mock = mock.MagicMock()
        response_mock.status = 400
        self.client._client.get.return_value.__aenter__.return_value = (  # type: ignore
            response_mock
        )

        with pytest.raises(ValueError, match="Invalid request.*"):
            await self.client._get(
                model=ModelTest,
                result_field="model",
                path="test",
            )


class PublicStashTest(IsolatedAsyncioTestCase):
    """Tests the public stash tab API client."""

    def setUp(self) -> None:
        """Setup override."""
        self.client = client.PoEClient("token", "test user agent")
        self.client._get = mock.AsyncMock()  # type: ignore
        return super().setUp()

    async def test_basic(self):
        """Basic test."""
        await self.client.get_public_stash_tabs()
        self.client._get.assert_called_with(  # type: ignore
            path="public-stash-tabs",
            model=PublicStash,
            query={},
        )

    async def test_next_change_id(self):
        """Tests the client when you use a next_change_id."""
        await self.client.get_public_stash_tabs(next_change_id="1234")
        self.client._get.assert_called_with(  # type: ignore
            path="public-stash-tabs",
            model=PublicStash,
            query={"id": "1234"},
        )
