from flask_restful import Resource, reqparse
from service.sessionService import SessionService
from flask_jwt_extended import jwt_required, get_jwt_identity


class SessionDetailsResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('session_token', required=True, help="session_token is a required field.")

    @jwt_required
    def post(self):
        session_service = SessionService()
        request = SessionDetailsResource.parser.parse_args()
        user = get_jwt_identity()
        response = session_service.get_session_details_for_user(request.get('session_token'), user)
        return response[0], response[1]
