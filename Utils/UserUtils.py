import Models
import json
import re
import Constants.userConstants as UserConstants
from Enums import UserEnums
from Dao.bookDAO import BookDAO


def validate_and_convert_new_user_request_object(aa: dict, bb: Models.User):
    for field in UserConstants.USER_MANDATORY_FIELDS:
        if field not in aa.keys():
            return f"Required field {field} is missing"
    return bb.from_json(json.dumps(aa))  # returns a dictionary


def convert_update_request_for_persistence(user_request, user_object):
    try:
        user_object.last_name = user_request.get(
            'last_name') if user_request.get('last_name') else user_object.last_name
        user_object.first_name = user_request.get(
            'first_name') if user_request.get('first_name') else user_object.first_name
        user_object.date_of_birth = user_request.get(
            'date_of_birth') if user_request.get('date_of_birth') else user_object.date_of_birth
        user_object.phone_number = user_request.get(
            'phone_number') if user_request.get('phone_number') else user_object.phone_number
        user_object.email = user_request.get(
            'email') if user_request.get('email') else user_object.email
        user_object.username = user_request.get(
            'username') if user_request.get('username') else user_object.username
        user_object.alt_username = user_request.get(
            'email').rsplit('@')[0] if user_request.get('email') else user_object.alt_username
        return user_object
    except Exception as e:
        return e


def convert_email_update_request_for_persistence(user_request, user_object):
    user_object.email = user_request.get('newEmail')
    return user_object


def convert_user_dto_to_public_response_dto(user):
    try:
        response_dto = dict()
        response_dto.setdefault('id', str(user.get('id')))
        response_dto.setdefault('first_name', user.get('first_name'))
        response_dto.setdefault('last_name', user.get('last_name') if user.get('last_name') else "")
        response_dto.setdefault('date_of_birth', str(user.get('date_of_birth')))
        response_dto.setdefault('email', user.get('email'))
        response_dto.setdefault('username', user.get('username'))
        return response_dto
    except Exception as e:
        print("DEBUG: Exception occurred in _USER_DTO_PUBLIC - {}".format(e))
        return "There was some error."


def convert_request_to_user_update_dto(request_dto, user_identity):
    try:
        response_user = clone_dto(user_identity)
        for field in UserConstants.USER_FIELDS_FOR_DETAILS_UPDATE:
            if field is not None:
                response_user[field] = request_dto[field]
        return response_user
    except Exception as e:
        return "Error: {}".format(e)


def clone_dto(user):
    _cloned_response = {}
    for field in user.keys():
        _cloned_response.setdefault(field, user.get(field))
    return _cloned_response


def is_length_valid_for_id_in_request(mongo_id) -> bool:
    if len(mongo_id) > 12*2 or len(mongo_id) < 12*2:
        return True
    return False


def validate_min_length(value, limit):
    if len(value) < int(limit):
        return False
    return True


def verify_username_length(curr, new):
    if len(curr) < UserEnums.MIN_USER_NAME_LENGTH.value or len(new) < UserEnums.MIN_USER_NAME_LENGTH.value:
        return [{'error': 'Invalid username length. Minimum username length should be 4.'}, 404]
    return False


def verify_email_length(curr, new):
    if len(curr) < UserEnums.MIN_EMAIL_LENGTH.value or len(new) < UserEnums.MIN_EMAIL_LENGTH.value:
        return [
            {
                'error':
                    'Invalid email length. Minimum email length should be 6. Please check your email and try again.'
            }, 404
        ]
    return False


def get_user_favourite_books(user):
    book_service = BookDAO()
    book_bucket = list()
    for book in user.fav_books:
        book_bucket.append(
            (
                book_service.find_active_book_by_id(book.id)
            )
        )
    return book_bucket
