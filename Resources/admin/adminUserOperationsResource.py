from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from service import userCreateUpdateService as UserCreateUpdateService


class AdminUserOperationsResource(Resource):
    @jwt_required
    def delete(self, user_email):
        current_user = get_jwt_identity()
        if not current_user['is_admin']:
            return {'error': 'Only admins can access this resource.'}, 403
        if not user_email:
            return {'response': {'error': 'Please provide an email Id.'}}
        resp = UserCreateUpdateService.delete_user(current_user, user_email)
        return {'response': resp[0]}, int(resp[1])
