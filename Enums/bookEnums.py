from enum import Enum


class BookEnums(Enum):
    PRIVACY_SCOPES_FOR_DOCUMENT = {"PUBLIC": "public-read", "PRIVATE": "private"}
    ALLOWED_EXTENSIONS = ["pdf", "epub", "mobi", "docx"]
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    RESTORE = "ACTIVE"
    DELETE = "INACTIVE"
    MAX_FILE_SIZE_ALLOWED_IN_MB_FOR_DOC = 10
