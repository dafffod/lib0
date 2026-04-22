from types import NoneType
import inspect
import traceback


class ExpliciteTypeError(Exception):
    def  __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

class TypeLockedError(Exception):
    def __init__(self, message: str) -> None:
         self.message = message
         super().__init__(self.message)

class ConstantAssignmentError(Exception):
    def __init__(self, message: str) -> None:
         self.message = message
         super().__init__(self.message)

class Lib0Error(Exception):
    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)
