"""holds all errors"""


class JsonError(Exception):
    def __init__(self, message):
        self.message = f"ERROR - Incorrect structure in input.json. {message}"
