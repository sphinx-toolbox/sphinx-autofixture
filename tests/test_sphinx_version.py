# stdlib
import os
import re

# 3rd party
import sphinx
from domdf_python_tools.compat import importlib_metadata


def test_sphinx_version_against_tox():
	m = re.match(r"py.*-sphinx(\d)\.(\d)", os.getenv("TOX_ENV_NAME", ''))
	if m is not None:
		target_version = tuple(map(int, m.groups()))
		assert target_version == sphinx.version_info[:2]


def test_pytest_version_against_tox():
	m = re.match(r"py.*-pytest(\d)\.(\d)", os.getenv("TOX_ENV_NAME", ''))
	if m is not None:
		target_version = tuple(map(int, m.groups()))
		pytest_version = tuple(map(int, importlib_metadata.version("pytest").split('.')[:2]))
		assert target_version == pytest_version
