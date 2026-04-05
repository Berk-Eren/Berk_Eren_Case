from urllib.parse import urljoin

from requests import Session


class CustomSession(Session):

    def __init__(self, base_url, *args, **kwargs):
        self.__base_url = base_url

        return super().__init__(*args, **kwargs)

    @property
    def base_url(self):
        return self.__base_url

    def request(self, method, url, *args, **kwargs):
        url = self.__base_url.rstrip("/") + "/" + url.lstrip("/")

        return super().request(method, url, *args, **kwargs)
