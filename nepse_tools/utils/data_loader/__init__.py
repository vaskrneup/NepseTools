"""
This module loads data from different paths for various purpose.
Additionally, it creates necessary files and folder for proper functioning of the script.
"""

import json


def load_test_data(filename: str) -> dict | list:
    """
    Loads Data from testing from `.test_data/{filename}`

    Args:
        filename: Name of the file from which to load test data

    Returns:
        dictionary, list or additional datatype depending on the filename

    """

    with open(f".test_data/{filename}", "r") as f:
        return json.loads(f.read())
