# stdlib
import asyncio
import builtins
import sys
from typing import Any, Callable, Dict

# 3rd party
import pytest_asyncio

__all__ = ["baz", "fizbuzz", "async_fixture"]

if sys.version_info >= (3, 7):
	# stdlib
	import dataclasses

	@dataclasses.dataclass()
	class A:
		"""
		My Dataclass
		"""

	__all__.append('A')


def foo():

	def bar():
		"""
		A locally defined function.
		"""

	return bar


baz = foo()
# fizbuzz = foo()


def create_fizbuzz():
	# Based on the dataclass module from CPython
	locals = {"BUILTINS": builtins}  # noqa: A001  # pylint: disable=redefined-builtin
	local_vars = ", ".join(locals.keys())

	txt = f" def fizbuzz(): pass"
	txt = f"def __create_fn__({local_vars}):\n{txt}\n return fizbuzz"

	ns: Dict[str, Any] = {}
	exec(txt, None, ns)
	return ns["__create_fn__"](**locals)


fizbuzz = create_fizbuzz()
fizbuzz.__qualname__ = "fizbuzz"
fizbuzz.__doc__ = "A locally defined function."


@pytest_asyncio.fixture(scope="module")
async def async_fixture():
	"""
	Async fixture demo
	"""

	return await asyncio.sleep(0.1)
