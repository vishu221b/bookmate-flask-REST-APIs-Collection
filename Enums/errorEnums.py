from enum import Enum


class ErrorEnums(Enum):
    UNAUTHORIZED_ERROR = {'error': 'You are unauthorized to access this resource.'}
    ALLOWED_SPECIAL_CHARACTERS = ['#', '@', '$', '!', '%', '*', '?', '&', '.', '+', '%', '_', '^']
    INVALID_PASSWORD_ERROR = {
        'error':
            "Invalid Password. Please check your password and try again.",
        'help': {
            '1': "Minimum length should be 8.",
            '2': "Should contain at least one digit, lowercase character and an uppercase character.",
            '3': "Should contain one special character.",
            '4': "Allowed special characters - {}".format(ALLOWED_SPECIAL_CHARACTERS)
        }
    }
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
    ID_MISSING_ERROR = {'error': 'Id is a required field. Please input an ID and try again.'}
    NO_BOOK_FOUND_ERROR = {'error': 'No book found.'}
    INACTIVE_BOOK_ERROR = {'error': 'Book is currently inactive.'}
    PROTECTED_BOOK_ACCESS_ERROR = {'error': 'Cannot access book as the book is not public.'}
    INVALID_EMAIL_FORMAT_ERROR = "Invalid email format. Please check your email and try again."
    INVALID_ID_FORMAT_ERROR = {'error': 'Invalid id detected. Please check your input and try again.'}
    BOOK_OWNER_NOT_MATCH_ERROR = {'error': 'Only book owner can update the book details.'}
    MAX_SIZE_EXCEED_ERROR_FOR_DOC = {'error': 'Maximum allowed file size is 10 MB.'}
