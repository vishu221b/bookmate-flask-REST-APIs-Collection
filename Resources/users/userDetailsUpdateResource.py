from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import service.userCreateUpdateService as UserCreateUpdateService
import Constants.userConstants as UserConstants
import Utils.UserUtils as UserConverterUtils
from Enums import AdminPermissionEnums


class UpdateUserDetails(Resource):
    parser = reqparse.RequestParser()
    for field in UserConstants.ALL_USER_FIELDS:
        parser.add_argument(field,
                            required=True if field in UserConstants.USER_UPDATE_MANDATORY_FIELDS else False,
                            help=field + 'cannot be left blank')

    @jwt_required
    def put(self):
        user_identity = get_jwt_identity()
        user_request = UpdateUserDetails.parser.parse_args()
        user_request = UserConverterUtils.convert_request_to_user_update_dto(user_request, user_identity)
        updated_user = UserCreateUpdateService.create_update_user(user_identity, user_request, True)
        if not isinstance(updated_user, str):
            updated_user = UserConverterUtils.convert_user_dto_to_public_response_dto(updated_user)
            return {
                'response': {
                            'updatedUser': updated_user
                }
            }, 200
        return {'error': updated_user}, 400

    @jwt_required
    def delete(self, user_email):
        try:
            current_user = get_jwt_identity()
            if not user_email:
                return {'response': {'error': 'Please provide an email Id.'}}, 404
            resp = UserCreateUpdateService.activate_deactivate_user(
                current_user, user_email, False, AdminPermissionEnums.DEACTIVATE.name)
            return resp[0], resp[1]
        except Exception as e:
            return {'error': e.args}, 400

    @jwt_required
    def post(self):
        return {"error": "Method not allowed."}, 405

    @jwt_required
    def get(self):
        return {'error': 'Method not allowed'}, 405
