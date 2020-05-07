from flask_restful import Resource
from Utils import UserUtils as UserConverter
from service import userCreateUpdateService as UserCreateUpdateService


class AllUserFetchResource(Resource):
    def get(self):
        all_users = []
        for i in UserCreateUpdateService.get_all_users():
            all_users.append(UserConverter.convert_user_dto_to_public_response_dto(i))
        return {'response': all_users}, 200
