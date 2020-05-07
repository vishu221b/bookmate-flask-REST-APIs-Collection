import Models
import json
import Constants.userConstants as UserConstants
from Utils import TimeUtils


def validate_and_convert_new_user_request_object(aa: dict, bb: Models.User):
    for field in UserConstants.USER_MANDATORY_FIELDS:
        if field not in aa.keys():
            return f"Required field {field} is missing"
    return bb.from_json(json.dumps(aa))  # returns a dictionary


def convert_update_request_for_persistence(user_request, user_object):
    user_object.last_name = user_request['last_name']
    user_object.first_name = user_request['first_name']
    user_object.date_of_birth = user_request['date_of_birth']
    user_object.phone_number = user_request['phone_number']
    return user_object


def convert_email_update_request_for_persistence(user_request, user_object):
    user_object.email = user_request['newEmail']
    return user_object


def user_dto(user):
    try:
        return {
            'id': str(user.pk),
            'first_name': user.first_name,
            'last_name': user.last_name if user.last_name else "",
            'date_of_birth': str(user.date_of_birth)[:10],
            'email': user.email,
            'phone_number': user.phone_number,
            'username': user.username,
            'is_active': user.is_active,
            'created_at': str(user.created_at),
            'password': str(user.password),
            'is_admin': bool(user.is_admin),
            'fav_books': list(user.fav_books),
        }
    except Exception as e:
        print("Error UDTO:2=>{}".format(e))


def convert_user_dto_to_public_response_dto(user):
    try:
        return {
            'id': user['id'],
            'first_name': user["first_name"],
            'last_name': user["last_name"] if user["last_name"] else "",
            'date_of_birth': str(user["date_of_birth"]),
            'email': user["email"],
            'phone_number': user["phone_number"],
            'username': user["username"],
            'is_active': user["is_active"],
            'created_at': str(user["created_at"]),
        }
    except Exception as e:
        print("Error URC:2=>{}".format(e))
        return "There was some error."


def convert_request_to_user_update_dto(request_dto, user_identity):
    try:
        request_dto['date_of_birth'] = TimeUtils.convert_time(request_dto['date_of_birth']) if request_dto['date_of_birth'] else None
        response_user = clone_dto(user_identity)
        for field in UserConstants.USER_FIELDS_FOR_GENERIC_UPDATE:
            if field is not None:
                response_user[field] = request_dto[field]
        return response_user
    except Exception as e:
        return "Error: {}".format(e)


def clone_dto(user):
    response_cloned = {}
    for field in user.keys():
        response_cloned[field] = user[field]
    return response_cloned


def is_length_valid_for_id_in_request(mongo_id) -> bool:
    if len(mongo_id) > 12*2 or len(mongo_id) < 12*2:
        return True
    return False


def validate_length(par, length):
    if len(par) < int(length):
        return False
    return True


def verify_username_length(curr, new):
    if len(curr) < 4 or len(new) < 4:
        return [{'error': 'Invalid username length. Minimum username length should be 4.'}, 404]
    return False


def verify_email_length(curr, new):
    if len(curr) < 6 or len(new) < 6:
        return [{
            'error': 'Invalid email length. Minimum email length should be 6. Please check your email and try again.'},
            404]
    return False
