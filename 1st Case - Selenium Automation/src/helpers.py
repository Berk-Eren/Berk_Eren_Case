from urllib.parse import urlencode, urlparse, urlunparse, quote


def build_url(base_url, path="/", params={}):
    url = base_url.rstrip("/") + "/" + path.strip("/")

    query = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())

    parsed = urlparse(url.lstrip("/"))
    return urlunparse(parsed._replace(query=query))
