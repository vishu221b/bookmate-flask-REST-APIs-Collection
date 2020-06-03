from flask_restful import Resource
from Utils import UserUtils as UserConverter
from service import userCreateUpdateService as UserCreateUpdateService
from flask_jwt_extended import jwt_optional, get_jwt_identity
from Enums import ErrorEnums


class UserFetchResource(Resource):
    @jwt_optional
    def get(self, scope):
        if scope.upper() == "ALL":
            all_users = []
            for i in UserCreateUpdateService.get_all_users():
                all_users.append(UserConverter.convert_user_dto_to_public_response_dto(i))
            return {'response': all_users}, 200
        user = get_jwt_identity()
        if not user:
            return {'error': ErrorEnums.SESSION_NOT_FOUND_ERROR.value}, 403
        if len(scope) != 24:
            return ErrorEnums.INVALID_ID_FORMAT_ERROR.value, 400
        user = UserCreateUpdateService.get_existing_user_by_id(scope)
        if 'error' in user.keys():
            return user, 404
        return UserConverter.convert_user_dto_to_public_response_dto(user), 200


