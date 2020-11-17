# 3rd party
import pytest
from pytest import fixture

# this package
from sphinx_autofixture import is_fixture


@fixture
def name():
	"""
	:return:
	"""


@fixture()
def call():
	"""

	:return:
	"""


@fixture(scope="module")
def call_scoped():
	"""

	:return:
	"""


@pytest.fixture
def pytest_attribute():
	"""
	:return:
	"""


@pytest.fixture()
def pytest_call():
	"""

	:return:
	"""


@pytest.fixture(scope="module")
def pytest_call_scoped():
	"""
	:return:
	"""


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
def test_is_fixture(func, scope):
	assert is_fixture(func) == (True, scope)


def function():
	pass


class Class:

	def method(self):
		pass


def deco(func):
	return func


@deco
def decorated():
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
def test_isnt_fixture(func):
	assert is_fixture(func) == (False, None)
