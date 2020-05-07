from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_raw_jwt
from service.userLoginService import revoke_session_token, get_revoked_tokens


class Logout(Resource):
    @jwt_required
    def delete(self):
        jti = get_raw_jwt()['jti']
        revoke_session_token(jti)
        return {'response': 'Successfully logged out.'}, 200
