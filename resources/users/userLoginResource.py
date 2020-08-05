from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, decode_token
from utils.TimeUtils import TimeUtils
from service.sessionService import SessionService
from service import userLoginService as UserLoginService
from service import userCreateUpdateService
from enums import AdminPermissionEnums


class Login(Resource):
    args = ['username', 'password', 'email']
    parser = reqparse.RequestParser()
    for arg in args:
        parser.add_argument(arg,
                            type=str,
                            required=True if arg == 'password' else False,
                            help=arg + ' is required')

    def post(self):
        try:
            time = TimeUtils()
            session_service = SessionService()
            login_args = Login.parser.parse_args()
            if login_args.get('username'):
                user = UserLoginService.get_by_username(login_args.get('username'))
                req_pass = UserLoginService.convert_password(login_args.get('password'))
                if not user:
                    return {'error': 'No such user. Please check your username.'}, 404
                if isinstance(user, str):
                    return {'error': user}, 404
                if str(user['password']) == req_pass:
                    if not user.get('is_active'):
                        userCreateUpdateService.activate_deactivate_user(
                            user, user.get('email'), False, AdminPermissionEnums.ACTIVATE.name)
                        user.__setitem__('is_active', True)
                    access_token = session_service.generate_session_token(user)
                    return {
                        'access_token': access_token,
                        'expiry': str(time.format_epoch_to_date_time(decode_token(access_token).get('exp')))
                    }, 200
            elif login_args.get('email'):
                user = UserLoginService.get_by_email(login_args.get('email'))
                req_pass = UserLoginService.convert_password(login_args.get('password'))
                if not user:
                    return {'error': 'No such user. Please check your email.'}, 401
                if isinstance(user, str):
                    return {'error': user}, 404
                if str(user['password']) == req_pass:
                    if not user.get('is_active'):
                        userCreateUpdateService.activate_deactivate_user(
                            user, user.get('email'), False, AdminPermissionEnums.ACTIVATE.name)
                        user.__setitem__('is_active', True)
                    access_token = session_service.generate_session_token(user)
                    return {
                        'access_token': access_token,
                        'expiry': str(time.format_epoch_to_date_time(decode_token(access_token).get('exp')))
                    }, 200
            return {'error': 'Invalid credentials.'}, 401
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400

    @jwt_required
    def get(self):
        try:
            user = get_jwt_identity()
            verified_user = UserLoginService.get_by_email(user.get('email'))
            if not isinstance(verified_user, str):
                return verified_user
            return {'error': verified_user}, 403
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400
