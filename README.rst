========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |github-actions| |travis| |appveyor| |requires|
        | |codecov|
    * - package
      - | |version| |wheel| |supported-versions| |supported-implementations|
        | |commits-since|
.. |docs| image:: https://readthedocs.org/projects/dmriprep_analyses/badge/?style=flat
    :target: https://dmriprep_analyses.readthedocs.io/
    :alt: Documentation Status

.. |travis| image:: https://api.travis-ci.com/GalBenZvi/dmriprep_analyses.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.com/github/GalBenZvi/dmriprep_analyses

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/GalBenZvi/dmriprep_analyses?branch=master&svg=true
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/GalBenZvi/dmriprep_analyses

.. |github-actions| image:: https://github.com/GalBenZvi/dmriprep_analyses/actions/workflows/github-actions.yml/badge.svg
    :alt: GitHub Actions Build Status
    :target: https://github.com/GalBenZvi/dmriprep_analyses/actions

.. |requires| image:: https://requires.io/github/GalBenZvi/dmriprep_analyses/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/GalBenZvi/dmriprep_analyses/requirements/?branch=master

.. |codecov| image:: https://codecov.io/gh/GalBenZvi/dmriprep_analyses/branch/master/graphs/badge.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/GalBenZvi/dmriprep_analyses

.. |version| image:: https://img.shields.io/pypi/v/niparser.svg
    :alt: PyPI Package latest release
    :target: https://pypi.org/project/niparser

.. |wheel| image:: https://img.shields.io/pypi/wheel/niparser.svg
    :alt: PyPI Wheel
    :target: https://pypi.org/project/niparser

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/niparser.svg
    :alt: Supported versions
    :target: https://pypi.org/project/niparser

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/niparser.svg
    :alt: Supported implementations
    :target: https://pypi.org/project/niparser

.. |commits-since| image:: https://img.shields.io/github/commits-since/GalBenZvi/dmriprep_analyses/v0.0.0.svg
    :alt: Commits since latest release
    :target: https://github.com/GalBenZvi/dmriprep_analyses/compare/v0.0.0...master



.. end-badges

A package to process data derived from dmriprep pipeline

* Free software: Apache Software License 2.0

Installation
============

::

    pip install niparser

You can also install the in-development version with::

    pip install https://github.com/GalBenZvi/dmriprep_analyses/archive/master.zip


Documentation
=============


https://dmriprep_analyses.readthedocs.io/


Development
===========

To run all the tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
