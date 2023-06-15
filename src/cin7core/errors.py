from typing import Optional

from requests import Response


class Cin7CoreException(Exception):
    def __init__(self, message: str, response: Optional[Response] = None):
        super().__init__(message)
        self.response = response


class AuthenticationError(Cin7CoreException):
    pass


class InvalidMethodError(Cin7CoreException):
    pass


class ListObjectsError(Cin7CoreException):
    pass


class GetObjectError(Cin7CoreException):
    pass


class CreateObjectError(Cin7CoreException):
    pass


class UpdateObjectError(Cin7CoreException):
    pass


class DeleteObjectError(Cin7CoreException):
    pass
