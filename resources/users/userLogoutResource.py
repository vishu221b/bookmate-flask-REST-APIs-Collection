from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_raw_jwt
from service.sessionService import SessionService


class Logout(Resource):
    @jwt_required
    def delete(self):
        try:
            session_service = SessionService()
            jti = get_raw_jwt()['jti']
            session_service.revoke_session_token(jti)
            return {'response': 'Successfully logged out.'}, 200
        except Exception as e:
            return {'error': f"Exception --  {e}  -- occurred."}, 500
