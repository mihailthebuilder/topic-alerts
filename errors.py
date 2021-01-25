"""holds all errors"""


class Error(Exception):
    pass


class AlertError(Error):
    def __init__(self, message):
        self.message = message
