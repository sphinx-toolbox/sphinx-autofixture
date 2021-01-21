#!/usr/bin/env python3
#
#  __init__.py
"""
Sphinx autodocumenter for pytest fixtures.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
import ast
import inspect
from types import FunctionType, MethodType
from typing import Any, Dict, Optional, Tuple, Union

# 3rd party
from domdf_python_tools.stringlist import StringList
from sphinx.application import Sphinx
from sphinx.config import Config
from sphinx.domains import ObjType
from sphinx.domains.python import PyClasslike, PyXRefRole
from sphinx.ext.autodoc import FunctionDocumenter, Options
from sphinx.ext.autodoc.directive import DocumenterBridge
from sphinx.locale import _

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.2.3"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["FixtureDecoratorFinder", "FixtureDocumenter", "is_fixture", "setup"]


class FixtureDecoratorFinder(ast.NodeVisitor):
	"""
	:class:`ast.NodeVisitor` for finding pytest fixtures.
	"""

	def __init__(self):

		#: Is the function a fixture?
		self.is_fixture = False

		#: If it is, the scope of the fixture.
		self.scope = "function"

	def visit_FunctionDef(self, node: ast.FunctionDef) -> None:  # noqa: D102
		if node.decorator_list:
			for deco in node.decorator_list:

				if isinstance(deco, ast.Call):
					keywords: Dict[Optional[str], ast.expr] = {k.arg: k.value for k in deco.keywords}

					if "scope" in keywords:
						scope = keywords["scope"]
						if isinstance(scope, ast.Constant):
							self.scope = scope.value
						elif isinstance(scope, ast.Str):
							self.scope = scope.s
						else:  # pragma: no cover
							raise NotImplementedError(type(scope))

					deco = deco.func
				else:
					self.scope = "function"

				if isinstance(deco, ast.Name):
					if deco.id == "fixture":
						self.is_fixture = True
						return
				elif isinstance(deco, ast.Attribute):
					if deco.attr == "fixture":
						self.is_fixture = True
						return
				else:  # pragma: no cover
					raise NotImplementedError(str(type(deco)))


def is_fixture(function: Union[FunctionType, MethodType]) -> Tuple[bool, Optional[str]]:
	"""
	Returns whether the given function is a fixture, and the fixture's scope if it is.

	:param function:
	"""

	# TODO: should this be relaxed? It seems inspect.getsource can find these after all.
	#  But can they work as fixtures?
	if "<locals>" in function.__qualname__:
		# Can't get source code for these (issue #6)
		return False, None

	visitor = FixtureDecoratorFinder()

	try:
		source = inspect.getsource(function)
	except OSError:
		# May be encountered with dataclasses where there's no source for the dynamic methods (issue #6)
		return False, None

	try:
		visitor.visit(ast.parse(source))
	except IndentationError:
		# Triggered when trying to parse a method
		return False, None

	if not visitor.is_fixture:
		return False, None
	else:
		return True, visitor.scope


class FixtureDocumenter(FunctionDocumenter):
	"""
	Sphinx autodoc :class:`~sphinx.ext.autodoc.Documenter` for documenting pytest fixtures.
	"""

	objtype = "fixture"
	directivetype = "fixture"
	priority = 20
	object: Union[FunctionType, MethodType]  # noqa: A003  # pylint: disable=redefined-builtin

	def __init__(self, directive: DocumenterBridge, name: str, indent: str = '') -> None:
		super().__init__(directive, name, indent)
		self.options = Options(self.options.copy())

	@classmethod
	def can_document_member(
			cls,
			member: Any,
			membername: str,
			isattr: bool,
			parent: Any,
			) -> bool:
		"""
		Called to see if a member can be documented by this documenter.

		:param member: The member being checked.
		:param membername: The name of the member.
		:param isattr:
		:param parent: The parent of the member.
		"""

		if isinstance(member, FunctionType):
			return is_fixture(member)[0]
		else:  # pragma: no cover
			return False

	def add_directive_header(self, sig: str = '') -> None:
		"""
		Add the directive's header.

		:param sig: Unused -- fixtures have no useful signature.
		:no-default sig:
		"""

		# doc_lines = (self.object.__doc__ or '').splitlines()
		# docstring = StringList([dedent(doc_lines[0]) + dedent("\n".join(doc_lines))[1:]])
		# print(docstring)
		# input(">>>")

		super().add_directive_header('')

		self.add_line('', self.get_sourcename())
		self.add_line(
				f"   **Scope:** |nbsp| |nbsp| |nbsp| |nbsp| {is_fixture(self.object)[1]}",
				self.get_sourcename(),
				)


def validate_config(app: Sphinx, config: Config):
	r"""
	Validate the provided configuration values.

	:param app: The Sphinx app.
	:param config:
	"""

	rst_prolog: Union[str, StringList] = config.rst_prolog or ''

	nbsp_sub = ".. |nbsp| unicode:: 0xA0\n   :trim:"
	if nbsp_sub not in rst_prolog:
		rst_prolog = StringList(rst_prolog)
		rst_prolog.append(nbsp_sub)

	config.rst_prolog = str(rst_prolog)  # type: ignore


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup :mod:`sphinx_autofixture`.

	:param app: The Sphinx app.
	"""

	app.registry.domains["py"].object_types["fixture"] = ObjType(_("fixture"), "fixture", "function", "obj")
	app.add_directive_to_domain("py", "fixture", PyClasslike)
	app.add_role_to_domain("py", "fixture", PyXRefRole())

	app.add_autodocumenter(FixtureDocumenter)

	app.connect("config-inited", validate_config)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			}
