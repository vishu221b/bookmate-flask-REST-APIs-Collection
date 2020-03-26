from flask_restful import Resource, reqparse
from constants import userConstants as UserConstants
from flask_jwt_extended import get_jwt_identity, jwt_required
from service import userCreateUpdateService as UserCreateUpdateService


class UserNameUpdateResource(Resource):
    parser = reqparse.RequestParser()
    for field in UserConstants.PARSER_FIELDS_FOR_USERNAME_UPDATE:
        parser.add_argument(field, type=str, required=True, help="Missing {} field.".format(field))

    @jwt_required
    def patch(self):
        user_request = UserNameUpdateResource.parser.parse_args()
        current_user = get_jwt_identity()
        response = UserCreateUpdateService.update_user_name(current_user, user_request['oldUsername'], user_request['newUsername'])
        return {'response': response[0]}, int(response[1])

    @jwt_required
    def get(self):
        return {'error': 'Method not supported.'}

    @jwt_required
    def post(self):
        return {'error': 'Method not supported.'}

    @jwt_required
    def put(self):
        return {'error': 'Method not supported.'}

    @jwt_required
    def delete(self):
        return {'error': 'Method not supported.'}
