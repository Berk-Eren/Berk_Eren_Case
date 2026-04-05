from base64 import urlsafe_b64decode as b64decode


BASE_URL = b64decode("aHR0cHM6Ly9pbnNpZGVyb25lLmNvbQ==").decode()
JOB_SEARCH_SITE = b64decode("aHR0cHM6Ly9qb2JzLmxldmVyLmNvL2luc2lkZXJvbmU=").decode()

OUTPUT_FOLDER = "output"
