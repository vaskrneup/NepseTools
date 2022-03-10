from nepse_tools.exceptions import NepseToolsBaseException


class MeroshareBaseException(NepseToolsBaseException):
    """
    Base Exception for meroshare, Every exception raised by meroshare must inherit from this Exception.
    """
    pass


class MeroshareDataLoadError(MeroshareBaseException):
    """
    Exception raised when api request to Meroshare backend fails.
    """
    pass


class MeroshareLoginError(MeroshareBaseException):
    """
    Exception raised when performing authentication related tasks.
    """
    pass


class MeroshareShareApplicationError(MeroshareBaseException):
    """
    Exception raised when Application Error is encountered.
    """
    pass


class MeroshareClientIDNotFoundError(MeroshareBaseException):
    """
    Exception raised when client ID is not found, when using `DP` to find the client ID.
    """
    pass


class MeroshareCredentialChangeError(MeroshareBaseException):
    """
    Exception raised when changing of pin or password is not successful.
    """
    pass
