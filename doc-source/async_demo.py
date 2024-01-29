# stdlib
import asyncio

# 3rd party
import pytest_asyncio


@pytest_asyncio.fixture(scope="module")
async def async_fixture():
	"""
	Async fixture demo
	"""

	return await asyncio.sleep(0.1)
