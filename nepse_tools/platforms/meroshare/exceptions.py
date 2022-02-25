from nepse_tools.exceptions import NepseToolsBaseException


class MeroshareBaseException(NepseToolsBaseException):
    pass


class MeroshareDataLoadError(MeroshareBaseException):
    pass


class MeroshareLoginError(MeroshareBaseException):
    pass


class MeroshareShareApplicationError(MeroshareBaseException):
    pass


class MeroshareClientIDNotFoundError(MeroshareBaseException):
    pass


class MeroshareCredentialChangeError(MeroshareBaseException):
    pass
