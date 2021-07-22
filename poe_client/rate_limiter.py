import asyncio
import logging
from collections import defaultdict
from datetime import datetime, timedelta
from threading import Lock
from typing import DefaultDict, Dict, List, Optional


class PolicyState(object):
    current_hits: int
    restriction: int
    last_request: datetime

    def __init__(self, current_hits, restriction) -> None:
        """State of a single policy."""
        self.current_hits = current_hits
        self.restriction = restriction
        self.last_request = datetime.now()

    def reset(self) -> None:
        """Reset to default values."""
        self.restriction = 0
        self.current_hits = 0
        self.last_request = datetime.now()


class Policy(object):
    """Class for tracking an individual rate limit policy."""

    name: str
    max_hits: int
    period: int
    restriction: int
    state: PolicyState

    mutex: asyncio.Lock = asyncio.Lock()

    def __init__(self, name: str, max_hits: int, period: int, restriction: int):
        """Initialize a new policy."""
        self.name = name
        self.max_hits = max_hits
        self.period = period
        self.restriction = restriction
        self.state = PolicyState(current_hits=0, restriction=0)

    async def update_state(self, current_hits: int, restriction: int):
        """Update the state of the policy."""
        async with self.mutex:
            logging.info(
                "Updating state[{0}] to {1} hits, {2} restriction".format(
                    self.name, current_hits, restriction
                )
            )
            self.state = PolicyState(current_hits, restriction)

    async def get_semaphore(self) -> bool:
        """Check state to see if request is allowed."""
        logging.info("{0} = {1}".format(self.name, self.state.__dict__))
        # If last request was restricted, wait and allow
        if self.state.restriction:
            logging.info(
                "restricted. Sleeping for {0} seconds".format(self.state.restriction)
            )
            await asyncio.sleep(self.state.restriction + 1)
            return True

        # Reset state and allow if last request is older restriction time.
        if self.state.last_request > (datetime.now() + timedelta(seconds=self.period)):
            await self.update_state(0, 0)
            return True

        if self.state.current_hits >= self.max_hits:
            logging.info(
                "max hits reached. Sleeping for {0} seconds".format(self.period)
            )
            await asyncio.sleep(self.period + 1)
            return True

        # If we haven't reached the quota, increase and allow
        if self.state.current_hits < self.max_hits:
            await self.update_state(self.state.current_hits + 1, self.state.restriction)
            return True

        # Don't allow by default
        return False


class RateLimiter(object):
    """Class for supporting the PoE API rate limitation."""

    policies: Dict[str, Dict[str, Policy]] = {}
    mutex: asyncio.Lock = asyncio.Lock()

    async def parse_headers(self, headers) -> None:
        """Parse headers into policies."""
        async with self.mutex:

            if not headers.get("X-Rate-Limit-Policy"):
                return

            policy_name = headers["X-Rate-Limit-Policy"]

            rule_names = headers["X-Rate-Limit-Rules"].split(",")
            for rule_name in rule_names:
                policy_id = "{0}/{1}".format(policy_name, rule_name)
                for rule in headers["X-Rate-Limit-{0}".format(rule_name)].split(","):
                    hits, period, restriction = rule.split(":")

                    if policy_id not in self.policies:
                        self.policies[policy_id] = {}

                    self.policies[policy_id][period] = Policy(
                        rule,
                        int(hits),
                        int(period),
                        int(restriction),
                    )

                for state in headers["X-Rate-Limit-{0}-State".format(rule_name)].split(
                    ","
                ):
                    await self.policies[policy_id][state.split(":")[1]].update_state(
                        int(state.split(":")[0]),
                        int(state.split(":")[2]),
                    )

    async def get_semaphore(self, policy_name: str) -> bool:
        """Get a semaphore to make a request."""
        if len(self.policies) == 0:
            logging.info("No policies, do a blocking request")
            return False

        semaphores = []
        for name, policy in self.policies.items():
            if name.startswith(policy_name):
                logging.info("getting semaphore {0}".format(name))
                for limit in policy.values():
                    semaphores.append(limit.get_semaphore())

        if semaphores:
            await asyncio.wait(semaphores)
        return True
