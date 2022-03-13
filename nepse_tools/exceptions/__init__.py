"""
This file contains Exceptions that others inherit from or
contains main Exceptions that will be used by all child modules.

Contribution:
    You can add any number of exception here, if it meets the above-mentioned conditions.
"""

from typing import Any


class NepseToolsBaseException(Exception):
    """
    This is the base `Exception` that every other *Custom Exception* must inherit from.

    Examples:
        ```
        class MyCustomException(NepseToolsBaseException):
            pass
        ```
    """

    def __init__(self, *args, error_data: Any = None) -> None:
        """
        Args:
            *args: Arguments passed to base Exception.
            error_data: Error data that will be available when handling exception.
        """
        super(NepseToolsBaseException, self).__init__(*args)
        self.error_data = error_data
