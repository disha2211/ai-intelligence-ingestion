from urllib.parse import urlparse


def normalize_url(url: str) -> str:

    parsed = urlparse(url)

    scheme = parsed.scheme.lower()
    host = parsed.netloc.lower()

    path = parsed.path.rstrip("/")

    return (
        f"{scheme}://{host}{path}"
    )