from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, reqparse
from constants import userConstants as UserConstants
from service import userCreateUpdateService as UserCreateUpdateService


class UserPasswordUpdateResource(Resource):
    parser = reqparse.RequestParser()
    for field in UserConstants.PARSER_FIELDS_FOR_PASSWORD_UPDATE:
        parser.add_argument(field, required=True, help="{} field cannot be left blank.".format(field))

    @jwt_required
    def patch(self):
        current_user = get_jwt_identity()
        user_request = UserPasswordUpdateResource.parser.parse_args()
        update_user = UserCreateUpdateService.update_password(
            current_user,
            user_request['oldPassword'],
            user_request['newPassword'])
        return {'response': update_user[0]}, int(update_user[1])

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
