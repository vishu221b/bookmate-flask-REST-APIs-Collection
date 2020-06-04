from flask_restful import Resource, reqparse
from service.sessionService import SessionService
from flask_jwt_extended import jwt_required, get_jwt_identity


class AdminSessionDetailsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('session_token', required=True, help="session_token is a required field.")

    @jwt_required
    def post(self):
        try:
            user = get_jwt_identity()
            if not user.get('is_admin'):
                return {'error': 'Only admins can access this resource.'}, 403
            session_service = SessionService()
            request = AdminSessionDetailsResource.parser.parse_args()
            response = session_service.get_session_details_for_user(request.get('session_token'), user, True)
            return response[0], response[1]
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400
