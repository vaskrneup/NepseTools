import json


def load_test_data(filename):
    with open(f".test_data/{filename}", "r") as f:
        return json.loads(f.read())
