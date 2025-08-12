<h1 align="center">kitconcept.contentsync 🔄</h1>

<div align="center">

[![PyPI](https://img.shields.io/pypi/v/kitconcept.contentsync)](https://pypi.org/project/kitconcept.contentsync/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kitconcept.contentsync)](https://pypi.org/project/kitconcept.contentsync/)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/kitconcept.contentsync)](https://pypi.org/project/kitconcept.contentsync/)
[![PyPI - License](https://img.shields.io/pypi/l/kitconcept.contentsync)](https://pypi.org/project/kitconcept.contentsync/)
[![PyPI - Status](https://img.shields.io/pypi/status/kitconcept.contentsync)](https://pypi.org/project/kitconcept.contentsync/)


[![Code Quality](https://github.com/kitconcept/kitconcept.contentsync/actions/workflows/main.yml/badge.svg)](https://github.com/kitconcept/kitconcept.contentsync/actions/workflows/main.yml)

[![GitHub contributors](https://img.shields.io/github/contributors/kitconcept/kitconcept.contentsync)](https://github.com/kitconcept/kitconcept.contentsync)
[![GitHub Repo stars](https://img.shields.io/github/stars/kitconcept/kitconcept.contentsync?style=social)](https://github.com/kitconcept/kitconcept.contentsync)

</div>

**kitconcept.contentsync** syncronizes Person content items in a Plone Site


# Develop

## Running tests

### Run all tests

```bash
uv run pytest
```

### Run all tests, stop on first fail

```bash
uv run pytest -x --pdb
```

### Run tests in the file `test_clients_plone`


```bash
uv run pytest -k test_clients_plone
```


### Run tests that do not require the containers (Faster tests)

```bash
uv run pytest -m "not docker"
```
