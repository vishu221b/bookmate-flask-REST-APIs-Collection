ALL_USER_FIELDS = ["first_name", "last_name", "date_of_birth",
                   "phone_number", "email", "username",
                   "password", "is_active", "is_admin", "fav_books", "authored_books"]

USER_MANDATORY_FIELDS = ["first_name", "date_of_birth", "phone_number", "email", "username", "password"]

USER_UPDATE_MANDATORY_FIELDS = ["first_name", "last_name", "date_of_birth", "phone_number", "email"]

USER_FIELDS_FOR_DETAILS_UPDATE = ["first_name", "last_name", "date_of_birth", "phone_number", "email", "username"]

PARSER_FIELDS_FOR_EMAIL_UPDATE = ["oldEmail", "newEmail"]

PARSER_FIELDS_FOR_PASSWORD_UPDATE = ["oldPassword", "newPassword"]

PARSER_FIELDS_FOR_USERNAME_UPDATE = ["oldUsername", "newUsername"]