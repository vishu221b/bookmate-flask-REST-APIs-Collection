from enum import Enum


class BookEnums(Enum):
    PRIVACY_SCOPES_FOR_DOCUMENT = {"PUBLIC": "public-read", "PRIVATE": "private"}
    ALLOWED_EXTENSIONS = ["pdf", "epub", "mobi", "docx"]
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    RESTORE = "ACTIVE"
    DELETE = "INACTIVE"
