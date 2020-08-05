from flask_restful import Resource, reqparse
from utils import UserUtils as UserConverter
from service import userCreateUpdateService as UserCreateUpdateService
from flask_jwt_extended import jwt_optional, get_jwt_identity
from enums import ErrorEnums


class UserFetchResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('Id', type=str, location='args')

    @jwt_optional
    def get(self, scope):
        try:
            if scope.upper() == "ALL":
                all_users = []
                for i in UserCreateUpdateService.get_all_users():
                    all_users.append(UserConverter.convert_user_dto_to_public_response_dto(i))
                return {'response': all_users}, 200
            elif scope.upper() == "SINGLE":
                request = UserFetchResource.parser.parse_args()
                user = get_jwt_identity()
                if not user:
                    return {'error': ErrorEnums.SESSION_NOT_FOUND_ERROR.value}, 403
                if not request.get('Id'):
                    return ErrorEnums.ID_MISSING_ERROR.value, 400
                if len(request.get('Id')) != 24:
                    return ErrorEnums.INVALID_ID_FORMAT_ERROR.value, 400
                user = UserCreateUpdateService.get_existing_user_by_id(request.get('Id'))
                if 'error' in user.keys():
                    return user, 404
                return UserConverter.convert_user_dto_to_public_response_dto(user), 200
            else:
                return {'error': 'Unknown scope encountered. Please check your input.'}, 400
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400


