SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	poetry run mypy poe_client tests/**/*.py
	poetry run flake8 .
	poetry run doc8 -q docs

.PHONY: unit
unit:
	# We don't want to run manual tests in CI, since they expect API credentials to exist.
	poetry run pytest -m 'not manual'

.PHONY: package
package:
	poetry check
	poetry run pip check
	poetry run safety check --full-report

.PHONY: test
test: lint package unit

