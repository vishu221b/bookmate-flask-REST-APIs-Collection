from enum import Enum


class ErrorEnums(Enum):
    UNAUTHORIZED_ERROR = {'error': 'You are unauthorized to access this resource.'}
    INVALID_PASSWORD_LENGTH_ERROR = "Minimum length requirement for password is 8."
    INVALID_PHONE_LENGTH_ERROR = "Invalid phone number length. Please check your phone number."
    INACTIVE_USER_ERROR = "User is currently inactive."
    NO_USER_FOUND_ERROR = "No user found. Please check your input."
    INVALID_INPUT_SUPPLIED_ERROR = "Invalid input exception. Please check your input and try again."
    UNKNOWN_REQUEST_ERROR = 'Unknown request encountered. Please check your parameters.'
    EMAIL_ALREADY_EXISTS_ERROR = "The email id already exists with another user. Please use different address."
    USER_NAME_ALREADY_EXISTS = "The username already exists for another user. Please try a different username."
    EXCEPTION_ERROR = "Exception - {} - occurred at - {}."
    INVALID_TOKEN_EXCEPTION = "Please provide your own valid session token."
    SESSION_NOT_FOUND_ERROR = "No session found. Please check your session token."
    NO_BOOK_FOUND_ERROR = {'error': 'No book found.'}
    INACTIVE_BOOK_ERROR = {'error': 'Book cannot be updated as the book is currently inactive.'}

