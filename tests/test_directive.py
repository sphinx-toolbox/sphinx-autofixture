# stdlib
import os
from pathlib import Path

# 3rd party
import pytest
from bs4 import BeautifulSoup  # type: ignore
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.testing import min_version, only_version
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


@only_version("3.6", reason="Output differs on 3.6")
@pytest.mark.parametrize("page", ["index.html"], indirect=True)
def test_output_36(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)


@only_version("3.7", reason="Output differs on 3.7")
@pytest.mark.parametrize("page", ["index.html"], indirect=True)
def test_output_37(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)


@min_version("3.8", reason="Output differs on 3.6-3.7")
@pytest.mark.parametrize("page", ["index.html"], indirect=True)
def test_output(page: BeautifulSoup, file_regression: FileRegressionFixture):
	check_html_regression(page, file_regression)
