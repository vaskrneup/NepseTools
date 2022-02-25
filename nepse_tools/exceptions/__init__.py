from typing import Any


class NepseToolsBaseException(Exception):
    def __init__(self, *args, error_data: Any = None):
        super(NepseToolsBaseException, self).__init__(*args)
        self.error_data = error_data
