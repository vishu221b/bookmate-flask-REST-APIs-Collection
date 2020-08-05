from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
import service.userCreateUpdateService as UserCreateUpdateService
import constants.userConstants as UserConstants
import utils.UserUtils as UserConverterUtils
from enums import AdminPermissionEnums


class UpdateUserDetails(Resource):
    parser = reqparse.RequestParser()
    for field in UserConstants.USER_FIELDS_FOR_DETAILS_UPDATE:
        parser.add_argument(
            field,
            required=False,
        )

    @jwt_required
    def put(self):
        try:
            user_identity = get_jwt_identity()
            user_request = UpdateUserDetails.parser.parse_args()
            if not user_request:
                return {'response': 'Details already up to date.'}, 200
            user_request = UserConverterUtils.convert_request_to_user_update_dto(user_request, user_identity)
            updated_user = UserCreateUpdateService.create_update_user(user_identity, user_request, True)
            if not isinstance(updated_user, str):
                updated_user = updated_user
                return {
                    'response': {
                                'updatedUser': updated_user
                    }
                }, 200
            return {'error': updated_user}, 400
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400

    @jwt_required
    def delete(self, user_email):
        try:
            current_user = get_jwt_identity()
            if not user_email:
                return {'error': 'Please provide an email Id.'}, 404
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
