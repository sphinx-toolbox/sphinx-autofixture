# stdlib
import asyncio
from types import FunctionType, MethodType
from typing import Any, Union

# 3rd party
import pytest
import pytest_asyncio  # type: ignore[import]
from pytest import fixture  # noqa: PT013

# this package
from sphinx_autofixture import is_fixture


@fixture
def name() -> None:
	"""
	:return:
	"""


@fixture()
def call() -> None:
	"""

	:return:
	"""


@fixture(scope="module")
def call_scoped() -> None:
	"""

	:return:
	"""


@pytest.fixture  # noqa: PT001
def pytest_attribute() -> None:
	"""
	:return:
	"""


@pytest.fixture()
def pytest_call() -> None:
	"""

	:return:
	"""


@pytest.fixture(scope="module")
def pytest_call_scoped() -> None:
	"""
	:return:
	"""


@pytest_asyncio.fixture(scope="module")
async def async_fixture():
	"""
	Async fixture demo
	"""

	return await asyncio.sleep(0.1)


@pytest.mark.parametrize(
		"func, scope",
		[
				pytest.param(name, "function", id="name"),
				pytest.param(call, "function", id="call"),
				pytest.param(call_scoped, "module", id="call_scoped"),
				pytest.param(pytest_attribute, "function", id="pytest_attribute"),
				pytest.param(pytest_call, "function", id="pytest_call"),
				pytest.param(pytest_call_scoped, "module", id="pytest_call_scoped"),
				]
		)
def test_is_fixture(func: Union[FunctionType, MethodType], scope: str) -> None:
	assert is_fixture(func) == (True, scope, False)


def test_is_async_fixture() -> None:
	assert is_fixture(async_fixture) == (True, "module", True)


def function() -> None:
	pass


class Class:

	def method(self) -> None:
		pass


def deco(func: Any) -> Any:
	return func


@deco
def decorated() -> None:
	pass


@pytest.mark.parametrize(
		"func",
		[
				pytest.param(function, id="function"),
				pytest.param(decorated, id="decorated"),
				pytest.param(Class.method, id="Class.method"),
				pytest.param(Class().method, id="Class().method"),
				]
		)
def test_isnt_fixture(func: Union[FunctionType, MethodType]) -> None:
	assert is_fixture(func) == (False, None, False)
