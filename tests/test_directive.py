# stdlib
import os
from pathlib import Path

# 3rd party
import pytest
from bs4 import BeautifulSoup, element  # type: ignore
from domdf_python_tools.paths import PathPlus
from coincidence import max_version, min_version, not_pypy, only_pypy, only_version
from pytest_regressions.file_regression import FileRegressionFixture
from sphinx.testing.path import path
from sphinx_toolbox.testing import check_html_regression

pytest_plugins = "sphinx.testing.fixtures"


@pytest.fixture(scope="session")
def rootdir():
	rdir = PathPlus(__file__).parent.absolute() / "doc-test"
	(rdir / "test-root").maybe_make(parents=True)
	return path(rdir)


@pytest.fixture()
def content(app):
	app.build(force_all=True)
	yield app


@pytest.fixture()
def page(content, request) -> BeautifulSoup:
	pagename = request.param
	c = (content.outdir / pagename).read_text()

	yield BeautifulSoup(c, "html5lib")


@pytest.fixture()
def original_datadir(request) -> Path:
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
						"37",
						marks=[
								only_version("3.7", reason="Output differs on 3.7"),
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
								only_version("3.7", reason="Output differs on 3.7"),
								only_pypy("Output differs on PyPy")
								]
						),
				pytest.param(
						"38",
						marks=[
								min_version("3.8", reason="Output differs on 3.6-3.7"),
								max_version("3.9.99", reason="Output differs on 3.10")
								]
						),
				pytest.param("310", marks=only_version("3.10", reason="Output differs on 3.10")),
				]
		)
def test_output(page: BeautifulSoup, file_regression: FileRegressionFixture, version):
	check_html_regression(page, file_regression)
