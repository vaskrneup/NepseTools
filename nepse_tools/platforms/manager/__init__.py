"""
Contains Main Blueprint and base functions and vars required to develop other things.
"""


class PlatformManager:
    """
    Base class for managing the platform specific things. Provides base features for the platform to build upon.
    """
    BASE_URL: str
    LOGIN_REQUEST_URL: str
    LOGOUT_REQUEST_URL: str

    def __init__(self) -> None:
        pass
