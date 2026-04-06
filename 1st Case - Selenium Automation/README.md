# First task - Web Automation with Selenium

First task

## Requirements

- Python 3.14
- Poetry

## Installation

- Install poetry
  - pip install poetry
- Create virtual environment with poetry
  - poetry env use python (or to your python path, env use /usr/bin/python3.12)
- Install libraries into the virtual environment
  - poetry install

## Execution

- Run the following
  - python -m pytest
- You can also add several options as below
  - python -m pytest --driver (chrome|firefox)
- In case of any type of error, log file and screenshots are saved under '_output_' folder.
