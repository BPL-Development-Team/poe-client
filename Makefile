SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy poe_client tests
	poetry run flake8 .
	poetry run doc8 -q docs

# We don't want to run manual tests in CI, since they expect API credentials to exist.
.PHONY: unit
unit:
	poetry run pytest -m 'not manual'

.PHONY: package
package:
	poetry check
	poetry run pip check
# 70612 is most likely a false positive and won't be fixed by the jinja2 maintainers. https://github.com/pallets/jinja/issues/1994
	poetry run safety check --full-report --ignore=70612

.PHONY: test
test: lint package unit

