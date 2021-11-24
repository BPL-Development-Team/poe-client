# poe-client

[![Build Status](https://github.com/BPL-Development-Team/poe-client/workflows/test/badge.svg?branch=master&event=push)](https://github.com/BPL-Development-Team/poe-client/actions?query=workflow%3Atest)
[![codecov](https://codecov.io/gh/BPL-Development-Team/poe-client/branch/master/graph/badge.svg)](https://codecov.io/gh/BPL-Development-Team/poe-client)
[![Python Version](https://img.shields.io/pypi/pyversions/poe-client.svg)](https://pypi.org/project/poe-client/)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)

Async PoE API client with rate limit support.

Updated for Scourge League.

## WARNING
This project is in an pre-alpha stage and has not been tested properly in production. Use with caution.

## Features

- Asynchronous HTTP client based on aiohttp
- Up-to-date with all PoE API endpoints
- All PoE API types defined as Pydantic schemas (Can generate OpenAPI Specifications)
- 100% test coverage and style enforced with wemake's flake8
- Fully typed with pydantic and checked with mypy, [PEP561 compatible](https://www.python.org/dev/peps/pep-0561/)


## Limitations
There is no API endpoint only to fetch rate limit headers. This means that the Client is not aware of what rules exist until it makes a real request.
Thus, be aware that sending too many request at the same time leads to being rate limited. Try to batch by 5, we've seen this as a safe level of concurrency.

## Installation

```bash
pip install poe-client
```


## Example

Showcase how your project can be used:

```python
from typing import List
import os

from poe_client.client import Client, PoEClient
from poe_client.schemas.league import League

token = os.environ["POE_TOKEN"]
contact = os.environ["POE_CONTACT"]

if not token or not contact:
    raise EnvironmentError("Need to set both POE_TOKEN and POE_CONTACT")


client = PoEClient(
    token,
    "poe-client",
    "1.0",
    contact,
)

async def list_leagues():
    """List leagues."""
    leagues: List[League] = []
    async with client:
        leagues = await client.list_leagues()

    logging.info(leagues)
```

## License

[MIT](https://github.com/BPL-Development-Team/poe-client/blob/master/LICENSE)


## Credits

This project was generated with [`wemake-python-package`](https://github.com/wemake-services/wemake-python-package). Current template version is: [6cb0736bbc9cb53ee126e2297b8ed7029b5e1380](https://github.com/wemake-services/wemake-python-package/tree/6cb0736bbc9cb53ee126e2297b8ed7029b5e1380). See what is [updated](https://github.com/wemake-services/wemake-python-package/compare/6cb0736bbc9cb53ee126e2297b8ed7029b5e1380...master) since then.
