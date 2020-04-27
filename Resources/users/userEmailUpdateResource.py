from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from Constants import userConstants as UserConstants
import service.userCreateUpdateService as UserCreateUpdateService


class UserEmailUpdateResource(Resource):
    parser = reqparse.RequestParser()
    for field in UserConstants.PARSER_FIELDS_FOR_EMAIL_UPDATE:
        parser.add_argument(field, required=True, help="Missing {} field.".format(field))

    @jwt_required
    def patch(self):
        user_request = UserEmailUpdateResource.parser.parse_args()
        current_user_identity = get_jwt_identity()
        response = UserCreateUpdateService.update_user_email(
            current_user_identity,
            user_request['oldEmail'],
            user_request['newEmail'])
        return {'response': response[0]}, int(response[1])

    @jwt_required
    def get(self):
        return {'error': 'method not supported.'}, 405

    @jwt_required
    def put(self):
        return {'error': 'method not supported.'}, 405

    @jwt_required
    def post(self):
        return {'error': 'method not supported.'}, 405

    @jwt_required
    def delete(self):
        return {'error': 'method not supported.'}, 405
