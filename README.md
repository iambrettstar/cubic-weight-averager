# Cubic Weight Averager
Coding challenge for kogan.com:

_Using the provided (paginated) API, find the average cubic weight for all products in the "Air Conditioners" category._

## Pre-Requisites
 * [python (^3.8)](https://www.python.org/downloads/)
 * [poetry](https://python-poetry.org/docs/)

### Install dependencies
To install dependencies to your virtual environment:

#### Windows
Install all dependencies:
```console
C:\cubic-weight-averager>poetry install
```
To exclude dev dependencies, add the `--no-dev` option:
```console
C:\cubic-weight-averager>poetry install --no-dev
```

## Usage
Once installed using poetry, you can run the CLI command:
```console
C:\cubic-weight-averager>poetry run cli
```
Options are defaulted, more information can be found with CLI help:
```console
C:\cubic-weight-averager>poetry run cli --help
```

## Tests
The code is setup for some basic unit tests and static analysis.
### Unit tests
```console
C:\cubic-weight-averager>poetry run pytest
```

### Linting
```console
C:\cubic-weight-averager>poetry run flake8
```

### Dead code
```console
C:\cubic-weight-averager>poetry run vulture cwa --min-confidence 70
```

### Security Checks
```console
C:\cubic-weight-averager>poetry run bandit -r cwa
```
