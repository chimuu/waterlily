from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class UserAlreadyExists(IntegrityError):
    """
    Raised when given username is already present in database
    """


class MobileAlreadyExists(IntegrityError):
    """
    Raised when given mobile no is already present in database
    """


class InvalidMobileError(ObjectDoesNotExist):
    """
    Raised when given mobile does not exist in database
    """


class InvalidOTPError(Exception):
    """
    Raised when given otp is invalid or expired
    """
