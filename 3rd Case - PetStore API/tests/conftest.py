import pytest

from src.session import CustomSession


@pytest.fixture(scope="class")
def session():
    return CustomSession(base_url="https://petstore.swagger.io/v2/pet/")
