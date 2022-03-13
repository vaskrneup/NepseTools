"""
Base Classes for managing the session. This contains basic request management methods.

Usage:
    Could be used as a mixin or a inherited class to implement `GET` and `POST` request.

Contribution:
    You can contribute other classes to manage requests in a better manner, but don't modify SessionManager.

    *NOTE: Write tests if possible*
"""

import requests


class SessionManager:
    """
    Manages the basic session for `GET` and `POST` request.
    Could be inherited and modified to implement additional features or persist session.

    Examples:
        ```
        SessionManager.get("https://example.com", ..., foo=bar)
        SessionManager.post("https://example.com", ..., foo=bar)
        SessionManager.request("https://example.com", ..., method="GET", foo=bar)
        ```
    """

    HEADERS: dict = {  # Initial Headers for making request.
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    }

    def __init__(self) -> None:
        self.session = requests
        self.session_headers = self.HEADERS

    def get(self, url: str, *args, **kwargs) -> requests.Response:
        """
        Direct implementation of HTML `GET` method.

        Examples:
            ```
            SessionManager().get("https://example.com", ..., foo=bar)
            ```

        Args:
            url: Url to make `GET` request to.
            *args: list value arguments that is passed to `requests.Session`
            **kwargs: key, value arguments that is passed to `requests.Session`

        Returns:
            Response from `requests.Session` or `requests.get`

        """

        resp = self.session.get(
            url, *args, headers=self.session_headers, **kwargs
        )

        return resp

    def post(self, url: str, *args, **kwargs) -> requests.Response:
        """
        Direct implementation of HTML `POST` method.

        Examples:
            ```
            SessionManager.post("https://example.com", ..., foo=bar)
            ```

        Args:
            url: Url to make `POST` request to.
            *args: list value arguments that is passed to `requests.Session`
            **kwargs: key, value arguments that is passed to `requests.Session`

        Returns:
            Response from `requests.Session` or `requests.get`

        """

        resp = self.session.post(
            url, *args, headers=self.session_headers, **kwargs
        )
        return resp

    def request(self, method: str, url: str, *args, **kwargs) -> requests.Response:
        """
        Implicit implementation of HTML `GET` and `POST` methods.

        Examples:
            ```
            SessionManager.request("https://example.com", ..., method="GET", foo=bar)
            ```

        Args:
            method: Method to be used for sending request.
            url: Url to send request to.
            *args: Args passed to `self.get` or `self.post`.
            **kwargs: Kwargs passed to `self.get` or `self.post`

        Returns:
            Response from either `self.get` or `self.post`

        """

        if method == "GET":
            return self.get(url, *args, **kwargs)
        elif method == "POST":
            return self.post(url, *args, **kwargs)
        else:
            raise ValueError(f"method got: {method}, expected `GET`, `POST`.")
