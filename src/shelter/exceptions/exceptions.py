from typing import Any

class PasswordError(Exception):

    def __init__(self, message:str, value: Any):
        super().__init__()
        self.message = message
        self.value = value

    def __str__ (self):
        return f"{self.message} (Value: {self.value})"