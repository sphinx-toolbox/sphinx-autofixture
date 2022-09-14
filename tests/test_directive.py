# stdlib
import os
from pathlib import Path
from typing import Any, Iterator

# 3rd party
import pytest
from bs4 import BeautifulSoup, element  # type: ignore[import]
from coincidence import max_version, min_version, not_pypy, only_pypy, only_version
from domdf_python_tools.paths import PathPlus
from sphinx.application import Sphinx
from sphinx.testing.path import path
from sphinx_toolbox.testing import HTMLRegressionFixture

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
	c = (content.outdir / pagename).read_text()

	yield BeautifulSoup(c, "html5lib")


@pytest.fixture()
def original_datadir(request: Any) -> Path:
	# Work around pycharm confusing datadir with test file.
	return PathPlus(os.path.splitext(request.module.__file__)[0] + '_')


@pytest.mark.parametrize("page", ["index.html"], indirect=True)
@pytest.mark.parametrize(
		"version",
		[
				pytest.param(
						"36",
						marks=[
								only_version("3.6", reason="Output differs on 3.6"),
								not_pypy("Output differs on PyPy")
								]
						),
				pytest.param(
						"36-pypy",
						marks=[
								only_version("3.6", reason="Output differs on 3.6"),
								only_pypy("Output differs on PyPy")
								]
						),
				pytest.param(
						"37-pypy",
						marks=[
								min_version("3.7", reason="Output differs on 3.7"),
								only_pypy("Output differs on PyPy")
								]
						),
				pytest.param(
						"37",
						marks=[
								min_version("3.7", reason="Output differs on 3.6"),
								max_version("3.9.99", reason="Output differs on 3.10"),
								not_pypy("Output differs on PyPy"),
								]
						),
				pytest.param("310", marks=min_version("3.10", reason="Output differs on 3.10")),
				]
		)
def test_output(
		page: BeautifulSoup,
		html_regression: HTMLRegressionFixture,
		version: str,
		) -> None:

	code: element.Tag
	for code in page.find_all("code", attrs={"class": "sig-prename descclassname"}):

		first_child = code.contents[0]
		if isinstance(first_child, element.Tag):
			code.contents = [first_child.contents[0]]

	for code in page.find_all("code", attrs={"class": "sig-name descname"}):
		first_child = code.contents[0]
		if isinstance(first_child, element.Tag):
			code.contents = [first_child.contents[0]]

	html_regression.check(page, jinja2=True)
