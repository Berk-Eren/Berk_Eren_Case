import json
import os

from jsonschema import validate


def is_schema_right(response, file_path) -> tuple[bool, None | Exception]:
    is_matched = False
    exception = None

    if file_path.endswith(".json") and os.path.isfile(file_path):
        with open(file_path, "r") as f:
            schema = json.load(f)

    try:
        validate(instance=response, schema=schema)
        is_matched = True
    except Exception as exc:
        is_matched = False
        exception = exc

    return is_matched, exception
