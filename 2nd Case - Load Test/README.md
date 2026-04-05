# 2nd Case - Load Test with Locust

This is the 2nd case fot load testing

## Requirements

- Python 3.14

## Intallation

- Install poetry
  - pip install poetry
- Create/use virtual environment
  - poetry env use python (or give direct path instead of only 'python')
- Install libraries
  - poetry install

## Execution

- You can run the following command
  - poetry run locust -f locust_file.py --host=https://www.n11.com --users 1 --spawn-rate 1 --run-time 30s --headless --print-stats --html index.html

<b>Note:</b> Unfortunately this script can't access to the website through Locust (return 403, Unauthorized), but I wanted to show the functionality of load test.
