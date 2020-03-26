from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
from service import userLoginService as UserLoginService


class Login(Resource):
    args = ['username', 'password', 'email']
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(arg,
                            type=str,
                            required=True if arg == 'password' else False,
                            help=arg + ' is required')

    def post(self):
        login_args = Login.parser.parse_args()
        if login_args['username']:
            user = UserLoginService.get_by_username(login_args['username'])
            req_pass = UserLoginService.convert_password(login_args['password'])
            if not user:
                return {'message': 'No such user. Please check your Username/Email and password and try again.'}, 404
            if isinstance(user, str):
                return {'error': user}, 404
            if str(user['password']) == req_pass:
                access_token = UserLoginService.generate_session_token(user)
                return {'access_token': access_token}, 200

        if login_args['email']:
            user = UserLoginService.get_by_email(login_args['email'])
            req_pass = UserLoginService.convert_password(login_args['password'])
            if not user:
                return {'error': 'No such user. Please check your Username/Email and password and try again.'}, 401
            if isinstance(user, str):
                return {'error': user}, 404
            if str(user['password']) == req_pass:
                access_token = UserLoginService.generate_session_token(user)
                return {'access_token': access_token}, 200
        return {'error': 'Invalid credentials'}, 401

    @jwt_required
    def get(self):
        user = get_jwt_identity()
        if not user:
            return {'error': 'You are not authorised to access this Resource.'}, 401
        verified_user = UserLoginService.get_by_email(user['email'])
        if not isinstance(verified_user, str):
            return verified_user
        return {'error': verified_user}, 403
