# stdlib
import builtins
import sys
from typing import Any, Callable, Dict

__all__ = ["baz", "fizbuzz"]

# stdlib
import dataclasses


@dataclasses.dataclass()
class A:
	"""
		My Dataclass
		"""


__all__.append('A')


def foo() -> Callable:

	def bar():  # noqa: MAN002
		"""
		A locally defined function.
		"""

	return bar


baz = foo()
# fizbuzz = foo()


def create_fizbuzz():  # noqa: MAN002
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
