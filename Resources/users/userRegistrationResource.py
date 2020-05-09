from flask_restful import Resource, reqparse
from Dao.userDAO import UserDAO
from Utils import SecurityUtils as UserSecurity
import Utils.TimeUtils as TimeUtils
from service import userCreateUpdateService as UserCreateUpdateService
import Constants.userConstants as UserConstants


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    for field in UserConstants.ALL_USER_FIELDS:
        parser.add_argument(field,
                            type=str,  # if field not in ["phone_number", "is_active", "is_admin"] else int,
                            required=True if field in UserConstants.USER_MANDATORY_FIELDS else False,
                            help='{} is a mandatory required'.format(
                                field if field in UserConstants.USER_MANDATORY_FIELDS else None))

# # ---------------------------------------x-x-POST-x-x-----------------------------------------------
    def post(self):
        user_details = UserRegister.parser.parse_args()
        user_details['password'] = UserSecurity.encrypt_pass(user_details['password'])
        user_details['date_of_birth'] = TimeUtils.convert_time(user_details['date_of_birth'])
        is_exist_user = UserCreateUpdateService.confirm_if_username_or_email_exists_already_during_registration(
            user_details['email'], user_details['username'])
        if is_exist_user and is_exist_user['result']:
            return {"error": str(is_exist_user['value'])}, 409
        try:
            result = UserDAO.create_user(user_details)
            if isinstance(result, str):
                return {'response': result}, 400
            return {"result": result}, 201
        except Exception as e:
            result = e
            return {"error": result}, 404

# # ---------------------------------------x-x-GET-x-x-----------------------------------------------

    def put(self):
        return {'error': 'Method not supported'}

    def delete(self):
        return {'error': 'Method not supported'}