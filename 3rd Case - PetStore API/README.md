# PetStore API Testing

This project perform tests against https://petstore.swagger.io/ API service.

The tests are written with _pytest_ framework.

There are positive and negative scenarios available within the repository.

## Requirements

- Python 3.14

## Installation

- Install poetry with pip
  - pip install poetry
- Create/use your virtualn environment
  - poetry env use python (or to your python path, env use /usr/bin/python3.12)
- Install poetry libraries from pyproject.toml
  - poerty install --without dev
- Run the tests with the following command
  - poetry run python -m pytest
- You can also filter the tests by _positive_ and _negative_ tag.
  - poetry run python -m pytest -m (positive|negative)
