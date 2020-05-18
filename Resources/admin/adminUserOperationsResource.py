from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from service import userCreateUpdateService as UserCreateUpdateService
from Enums import ErrorEnums, AdminPermissionEnums


class AdminUserOperationsResource(Resource):
    @jwt_required
    def delete(self, user_email):
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return ErrorEnums.UNAUTHORIZATION_ERROR.value, 403
            if not user_email:
                return {'response': {'error': 'Please provide an email Id.'}}, 400
            resp = UserCreateUpdateService.activate_deactivate_user(current_user,
                                                                    user_email,
                                                                    True,
                                                                    AdminPermissionEnums.DEACTIVATE.name)
            return resp[0], resp[1]
        except Exception as e:
            return {'error': e.args}, 400

    @jwt_required
    def put(self, user_email, permission_type):
        try:
            user = get_jwt_identity()
            if not user.get('is_admin'):
                return ErrorEnums.UNAUTHORIZATION_ERROR.value, 403
            response = UserCreateUpdateService.admin_access(user, user_email, permission_type)
            return response[0], response[1]
        except Exception as e:
            return {'error': e.args}, 400

    @jwt_required
    def post(self, user_email):
        try:
            current_user = get_jwt_identity()
            if not current_user.get('is_admin'):
                return ErrorEnums.UNAUTHORIZATION_ERROR.value, 403
            if not user_email:
                return {'response': {'error': 'Please provide an email Id.'}}, 400
            resp = UserCreateUpdateService.activate_deactivate_user(current_user,
                                                                    user_email,
                                                                    True,
                                                                    AdminPermissionEnums.ACTIVATE.name)
            return resp[0], resp[1]
        except Exception as e:
            return {'error': e.args}, 400
