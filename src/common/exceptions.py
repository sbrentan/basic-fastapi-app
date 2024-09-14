from typing import Optional


class RequestException(Exception):

    def __init__(self, message, status_code: Optional[int] = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DatabaseException(Exception):

    def __init__(self, message, exception=None):
        self.message = message
        self.exception = exception
        super().__init__(self.message)

    def __str__(self):
        return self.message
