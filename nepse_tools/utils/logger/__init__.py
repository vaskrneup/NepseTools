from termcolor import colored
from os import system, name


class Logger:
    LOG_ERROR = True
    LOG_INFO = True
    LOG_WARNING = True
    LOG_SUCCESS = True
    PRINT_OUTPUT = True

    def __init__(self):
        if name == "nt":
            system("color")

    def log(self, message, output_manager):
        if self.PRINT_OUTPUT:
            print(output_manager(message))

    def info(self, msg):
        if self.LOG_INFO:
            self.log(msg, lambda txt: colored(f"[~] {txt}", "blue"))

    def error(self, msg):
        if self.LOG_ERROR:
            self.log(msg, lambda txt: colored(f"[-] {txt}", "red"))

    def success(self, msg):
        if self.LOG_SUCCESS:
            self.log(msg, lambda txt: colored(f"[+] {txt}", "green"))

    def warning(self, msg):
        if self.LOG_WARNING:
            self.log(msg, lambda txt: colored(f"[!] {txt}", "yellow"))


logger = Logger()
