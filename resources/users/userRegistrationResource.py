from flask_restful import Resource, reqparse
from service import userCreateUpdateService as UserCreateUpdateService
import constants.userConstants as UserConstants


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
        try:
            user_request_details = UserRegister.parser.parse_args()
            is_exist_user = UserCreateUpdateService.confirm_if_username_or_email_exists_already_during_registration(
                user_request_details.get('email'), user_request_details.get('username'))
            if is_exist_user and is_exist_user.get('result'):
                return {
                           "error": str(
                               is_exist_user.get('value')
                           )
                       }, 409
            result = UserCreateUpdateService.create_update_user(None, user_request_details, False)
            if isinstance(result, str):
                return {'error': result}, 400
            return {"response": result}, 201
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400

# # ---------------------------------------x-x-GET-x-x-----------------------------------------------

    def put(self):
        return {'error': 'Method not supported'}

    def delete(self):
        return {'error': 'Method not supported'}