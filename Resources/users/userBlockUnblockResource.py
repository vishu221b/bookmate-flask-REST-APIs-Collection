from flask_restful import Resource
from service import UserSocialService
from flask_jwt_extended import get_jwt_identity, jwt_required


class BlockUnblockUsers(Resource):
    @jwt_required
    def post(self, action: str, user_to_be_blocked_unblocked):
        try:
            requestor_user = get_jwt_identity()
            user_social_service = UserSocialService()
            response = user_social_service.block_unblock_a_user(
                requestor_user.get('email'), user_to_be_blocked_unblocked, action.upper())
            return response[0], response[1]
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400
