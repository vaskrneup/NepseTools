from copyreg import constructor
from email import header
import requests


class SessionManagerMixin:
    HEADERS = {}

    def __init__(self) -> None:
        self.session: requests.Session = requests.Session()

    def get(self, url: str, *args, **kwargs) -> requests.Response:
        return self.session.get(url, *args, headers=self.HEADERS, **kwargs)

    def post(self, url: str, *args, **kwargs) -> requests.Response:
        return self.session.post(url, *args, headers=self.HEADERS, **kwargs)

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        if method == "GET":
            return self.get(url, *args, **kwargs)
        elif method == "POST":
            return self.post(url, *args, **kwargs)
        else:
            raise ValueError(f"method got: {method}, expected `GET`, `POST`.")
