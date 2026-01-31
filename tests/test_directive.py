# stdlib
import os
import pathlib
from pathlib import Path
from typing import Any, Iterator, Tuple, Union, cast, no_type_check

# 3rd party
import pytest
import sphinx
from bs4 import BeautifulSoup, NavigableString, PageElement, Tag, element
from coincidence import max_version, min_version, not_pypy, only_pypy, only_version
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx
from sphinx_toolbox.testing import HTMLRegressionFixture

if sphinx.version_info >= (7, 2):
	path = pathlib.Path
else:
	# 3rd party
	from sphinx.testing.path import path  # type: ignore[assignment]

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir() -> path:
	rdir = PathPlus(__file__).parent.absolute() / "doc-test"
	(rdir / "test-root").maybe_make(parents=True)
	return path(rdir)


@pytest.fixture()
def content(app: Sphinx) -> Iterator[Sphinx]:
	app.build(force_all=True)
	yield app


@pytest.fixture()
def page(content: Any, request: Any) -> Iterator[BeautifulSoup]:
	pagename = request.param
	c = (content.outdir / pagename).read_text(encoding="UTF-8")

	yield BeautifulSoup(c, "html5lib")


@pytest.fixture()
def original_datadir(request: Any) -> Path:
	# Work around pycharm confusing datadir with test file.
	return PathPlus(os.path.splitext(request.module.__file__)[0] + '_')


only_36 = only_version("3.6", reason="Output differs on 3.6")
min_37 = min_version("3.7", reason="Output differs on 3.6")
not_pypy_mark = not_pypy("Output differs on PyPy")
only_pypy_mark = only_pypy("Output differs on PyPy")


@pytest.mark.parametrize("page", ["index.html"], indirect=True)
@pytest.mark.parametrize(
		"version",
		[
				pytest.param("36", marks=[only_36, not_pypy_mark]),
				pytest.param("36-pypy", marks=[only_36, only_pypy_mark]),
				pytest.param("37-pypy", marks=[min_37, only_pypy_mark]),
				pytest.param(
						"37",
						marks=[
								min_37,
								max_version("3.9.99", reason="Output differs on 3.10"),
								not_pypy_mark,
								],
						),
				pytest.param("310", marks=min_version("3.10", reason="Output differs on 3.10")),
				],
		)
def test_output(
		page: BeautifulSoup,
		html_regression: HTMLRegressionFixture,
		version: str,
		) -> None:

	code: Union[PageElement, Tag, NavigableString]
	for code in page.find_all("code", attrs={"class": "sig-prename descclassname"}):
		assert isinstance(code, Tag)
		first_child = code.contents[0]
		if isinstance(first_child, element.Tag):
			code.contents = [first_child.contents[0]]

	for code in page.find_all("code", attrs={"class": "sig-name descname"}):
		assert isinstance(code, Tag)
		first_child = code.contents[0]
		if isinstance(first_child, element.Tag):
			code.contents = [first_child.contents[0]]

	for div in page.find_all("script"):
		assert isinstance(div, Tag)
		if div.get("src"):
			div["src"] = cast(str, div["src"]).split("?v=")[0]
			print(div["src"])

	html_regression.check(page, jinja2=True, jinja2_namespace={"alabaster_version": _get_alabaster_version()})


@no_type_check
def _get_alabaster_version() -> Tuple[int, int, int]:
	try:
		# 3rd party
		import alabaster._version as alabaster  # type: ignore[import-untyped]
	except ImportError:
		# 3rd party
		import alabaster  # type: ignore[import-untyped]

	return tuple(map(int, alabaster.__version__.split('.')))
