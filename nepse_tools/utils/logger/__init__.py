"""
Logging Functionality for the package, Not the industry standard but is simple and intuitive.

Contribution:
    You are open to implement it as you like, but make sure log, info, error, success and warning methods do not change.
    You can add other methods and change the inner functionality too, but without breaking the current implementation.
"""
import typing

from termcolor import colored
from os import system, name


class Logger:
    """
    Simple logger to log messages in an easy-to-read format.

    Contribution:
        Feel free to add new methods and functionalities to this Class
    """

    LOG_ERROR = True
    LOG_INFO = True
    LOG_WARNING = True
    LOG_SUCCESS = True
    PRINT_OUTPUT = True

    def __init__(self):
        if name == "nt":  # Setting up support for colored print in Windows terminal.
            system("color")

    def log(
            self,
            message: typing.Any,
            output_manager: typing.Callable[[typing.Any], str]
    ) -> None:
        """
        Main method for logging message

        Args:
            message: Any data to be logged
            output_manager: Function that accepts the object and returns string after necessary formatting

        Returns:
            None

        """

        if self.PRINT_OUTPUT:
            print(output_manager(message))

    def info(self, msg: typing.Any) -> None:
        """
        Logs Message in blue color

        Args:
            msg: Any data to be logged

        Returns:
            None

        """

        if self.LOG_INFO:
            self.log(msg, lambda txt: colored(f"[~] {txt}", "blue"))

    def error(self, msg: typing.Any) -> None:
        """
        Logs error Message in red color

        Args:
            msg: Any data to be logged

        Returns:
            None

        """

        if self.LOG_ERROR:
            self.log(msg, lambda txt: colored(f"[-] {txt}", "red"))

    def success(self, msg: typing.Any) -> None:
        """
        Logs error Message in green color

        Args:
            msg: Any data to be logged

        Returns:
            None

        """

        if self.LOG_SUCCESS:
            self.log(msg, lambda txt: colored(f"[+] {txt}", "green"))

    def warning(self, msg: typing.Any) -> None:
        """
        Logs error Message in yellow color

        Args:
            msg: Any data to be logged

        Returns:
            None

        """

        if self.LOG_WARNING:
            self.log(msg, lambda txt: colored(f"[!] {txt}", "yellow"))


logger = Logger()
