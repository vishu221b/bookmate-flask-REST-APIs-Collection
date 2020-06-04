from enum import Enum


class UserEnums(Enum):
    MIN_PHONE_NUMBER_LENGTH = 9
    MAX_PHONE_NUMBER_LENGTH = 13
    MIN_USER_NAME_LENGTH = 4
    MIN_PASSWORD_LENGTH = 8
    MIN_EMAIL_LENGTH = 6
    MARK = [{'response': 'Book successfully marked as favourite.'}, 200]
    REMOVE = [{'response': 'Book successfully removed from favourites.'}, 200]
    BLOCK = "BLOCK"
    UNBLOCK = "UNBLOCK"
    FOLLOW = "FOLLOW"
    UNFOLLOW = "UNFOLLOW"
    VALID_EMAIL = '^([a-zA-Z0-9][a-zA-Z0-9.]+[@][a-zA-Z0-9]+[\\.][a-zA-Z0-9.]+)$'
    VALID_PASS = '^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[#@$!%*?&.+%_\\^])[\\w\\^#%@$!%*?&.+_]{8,}$'
