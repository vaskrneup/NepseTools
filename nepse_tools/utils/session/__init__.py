from copyreg import constructor
from email import header
import requests


class SessionManagerMixin:
    HEADERS: dict = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    def __init__(self) -> None:
        self.session = requests
        self.session_headers = self.HEADERS

    def get(self, url: str, *args, **kwargs) -> requests.Response:
        resp = self.session.get(
            url, *args, headers=self.session_headers, **kwargs
        )

        return resp

    def post(self, url: str, *args, **kwargs) -> requests.Response:
        resp = self.session.post(
            url, *args, headers=self.session_headers, **kwargs
        )
        return resp

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        if method == "GET":
            return self.get(url, *args, **kwargs)
        elif method == "POST":
            return self.post(url, *args, **kwargs)
        else:
            raise ValueError(f"method got: {method}, expected `GET`, `POST`.")
