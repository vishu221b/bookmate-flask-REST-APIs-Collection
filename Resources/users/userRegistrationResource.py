from flask_restful import Resource, reqparse
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
        is_exist_user = UserCreateUpdateService.confirm_if_username_or_email_exists_already_during_registration(
            user_details.get('email'), user_details.get('username'))
        if is_exist_user and is_exist_user.get('result'):
            return {
                       "error": str(
                           is_exist_user.get('value')
                       )
                   }, 409
        try:
            result = UserCreateUpdateService.create_update_user(None, user_details, False)
            if isinstance(result, str):
                return {'error': result}, 400
            return {"response": result}, 201
        except Exception as e:
            result = e
            return {"error": result}, 400

# # ---------------------------------------x-x-GET-x-x-----------------------------------------------

    def put(self):
        return {'error': 'Method not supported'}

    def delete(self):
        return {'error': 'Method not supported'}