import unittest
from unittest import mock
from yarl import URL

from poe_client import client

from poe_client.schemas import Model
from poe_client.schemas.stash import PublicStash


class ModelTest(Model):
    """Test Model."""

    thing: str


class ClientTest(unittest.IsolatedAsyncioTestCase):
    """Tests the POE client.

    Several lines have typing ignored because we're mocking out elements of
    the class for testing, which the typing system doesn't understand."""

    def setUp(self) -> None:
        self.client = client.PoEClient("token", "test user agent")
        self.client._base_url = URL("https://example.com")
        self.client._client = mock.AsyncMock()
        return super().setUp()

    async def test_complete(self):
        response_mock = mock.MagicMock()
        response_mock.status = 200
        response_mock.headers = {}
        response_mock.json = mock.AsyncMock(return_value={"model": {"thing": "1"}})
        self.client._client.get.return_value.__aenter__.return_value = response_mock  # type: ignore

        result = await self.client._get(
            model=ModelTest,
            result_field="model",
            path="test",
        )
        self.assertEqual(result, ModelTest(thing="1"))
        self.assertEqual(
            self.client._client.get.call_args,  # type: ignore
            mock.call(
                "https://example.com/test",
                headers={
                    "Authorization": "Bearer token",
                    "User-Agent": "test user agent",
                },
                params=None,
                raise_for_status=False,
            ),
        )

    async def test_no_result_field(self):
        response_mock = mock.MagicMock()
        response_mock.status = 200
        response_mock.headers = {}
        response_mock.json = mock.AsyncMock(return_value={"thing": "123"})
        self.client._client.get.return_value.__aenter__.return_value = response_mock  # type: ignore

        result = await self.client._get(
            model=ModelTest,
            path="test",
        )
        self.assertEqual(result, ModelTest(thing="123"))

    async def test_get_list(self):
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
        self.client._client.get.return_value.__aenter__.return_value = response_mock  # type: ignore

        result = await self.client._get_list(
            model=ModelTest,
            result_field="model",
            path="test",
        )
        self.assertEqual(result, [ModelTest(thing="12"), ModelTest(thing="98")])

    async def test_wrong_status(self):
        response_mock = mock.MagicMock()
        response_mock.status = 400
        self.client._client.get.return_value.__aenter__.return_value = response_mock  # type: ignore

        with self.assertRaises(ValueError):
            await self.client._get(
                model=ModelTest,
                result_field="model",
                path="test",
            )


class PublicStashTest(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.client = client.PoEClient("token", "test user agent")
        self.client._get = mock.AsyncMock()  # type: ignore
        return super().setUp()

    async def test_basic(self):
        await self.client.get_public_stash_tabs()
        self.client._get.assert_called_with(  # type: ignore
            path="public-stash-tabs", model=PublicStash, query={}
        )

    async def test_next_change_id(self):
        await self.client.get_public_stash_tabs(next_change_id="1234")
        self.client._get.assert_called_with(  # type: ignore
            path="public-stash-tabs", model=PublicStash, query={"id": "1234"}
        )
