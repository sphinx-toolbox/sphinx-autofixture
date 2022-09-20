###################
sphinx-autofixture
###################

.. start short_desc

**Sphinx autodocumenter for pytest fixtures.**

.. end short_desc

See `the documentation`_ for an example of the output with the Furo Sphinx theme,
and `the documentation for coincidence`_ for an example with the ReadTheDocs theme.

.. _the documentation: https://sphinx-autofixture.readthedocs.io/en/latest/usage.html#directive-autofixture
.. _the documentation for coincidence: https://coincidence.readthedocs.io/en/latest/api/fixtures.html

.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/sphinx-autofixture/latest?logo=read-the-docs
	:target: https://sphinx-autofixture.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/sphinx-toolbox/sphinx-autofixture/workflows/Docs%20Check/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/sphinx-toolbox/sphinx-autofixture/workflows/Linux/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/sphinx-toolbox/sphinx-autofixture/workflows/Windows/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/sphinx-toolbox/sphinx-autofixture/workflows/macOS/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/sphinx-toolbox/sphinx-autofixture/workflows/Flake8/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/sphinx-toolbox/sphinx-autofixture/workflows/mypy/badge.svg
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/sphinx-autofixture/badge.svg
	:target: https://dependency-dash.repo-helper.uk/github/sphinx-toolbox/sphinx-autofixture/
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/sphinx-toolbox/sphinx-autofixture/master?logo=coveralls
	:target: https://coveralls.io/github/sphinx-toolbox/sphinx-autofixture?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/sphinx-toolbox/sphinx-autofixture?logo=codefactor
	:target: https://www.codefactor.io/repository/github/sphinx-toolbox/sphinx-autofixture
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/sphinx-autofixture
	:target: https://pypi.org/project/sphinx-autofixture/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sphinx-autofixture?logo=python&logoColor=white
	:target: https://pypi.org/project/sphinx-autofixture/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sphinx-autofixture
	:target: https://pypi.org/project/sphinx-autofixture/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/sphinx-autofixture
	:target: https://pypi.org/project/sphinx-autofixture/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/sphinx-autofixture?logo=anaconda
	:target: https://anaconda.org/domdfcoding/sphinx-autofixture
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/sphinx-autofixture?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/sphinx-autofixture
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/sphinx-toolbox/sphinx-autofixture
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/sphinx-toolbox/sphinx-autofixture
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/sphinx-toolbox/sphinx-autofixture/v0.4.0
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/sphinx-toolbox/sphinx-autofixture
	:target: https://github.com/sphinx-toolbox/sphinx-autofixture/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2022
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/sphinx-autofixture
	:target: https://pypi.org/project/sphinx-autofixture/
	:alt: PyPI - Downloads

.. end shields

Installation
--------------

.. start installation

``sphinx-autofixture`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install sphinx-autofixture

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels https://conda.anaconda.org/conda-forge
		$ conda config --add channels https://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install sphinx-autofixture

.. end installation
