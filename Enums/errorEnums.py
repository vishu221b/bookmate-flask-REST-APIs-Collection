from enum import Enum


class ErrorEnums(Enum):
    UNAUTHORIZATION_ERROR = {'error': 'You are unauthorized to access this resource.'}
    INVALID_PASSWORD_LENGTH_ERROR = "Minimum length requirement for password is 8."
    INVALID_PHONE_LENGTH_ERROR = "Invalid phone number length. Please check your phone number."
