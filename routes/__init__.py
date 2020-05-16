from flask import redirect, send_from_directory
from service.sessionService import get_revoked_tokens


def initiate_routes(application, jwt):
    @application.route('/')
    def index():
        return redirect('/swagger')

    @application.route('/static/<path>')
    def swag_route(path):
        return send_from_directory('static', path)

    @jwt.token_in_blacklist_loader
    def check_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        bucket = get_revoked_tokens()
        return str(jti) in bucket

    @jwt.revoked_token_loader
    def revoked_token_check_callback():
        return {
                   application.config[
                       'JWT_ERROR_MESSAGE_KEY']: 'Your session has expired. Please login again to continue.'
               }, 401

    @jwt.expired_token_loader
    def expired_token_check_callback():
        return {
                   application.config[
                       'JWT_ERROR_MESSAGE_KEY']: 'Your session has expired. Please login again to continue.'
               }, 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
                   application.config['JWT_ERROR_MESSAGE_KEY']: "Invalid token exception.",
                   "exceptionMessage": f"{error}."
               }, 422

    @jwt.unauthorized_loader
    def unauthorized_token_callback(error):
        return {
                   application.config['JWT_ERROR_MESSAGE_KEY']: "Exception encountered.",
                   "exceptionMessage": f"{error}."
               }, 401
