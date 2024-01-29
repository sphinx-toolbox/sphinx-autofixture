"""
Minimal skeleton necessary for tests.
"""

# stdlib
import functools

# 3rd party
import pytest


def fixture(fixture_function=None, **kwargs):
	if fixture_function is not None:
		if hasattr(fixture_function, "__func__"):
			fixture_function = fixture_function.__func__
		fixture_function._force_asyncio_fixture = True
		return pytest.fixture(fixture_function, **kwargs)

	else:

		@functools.wraps(fixture)
		def inner(fixture_function):
			return fixture(fixture_function, **kwargs)

		return inner
