from flask import Flask, send_from_directory, redirect, url_for
from flask_restful import Api
from flask_jwt_extended import JWTManager
import Resources
import DB
from service.userLoginService import get_revoked_tokens
from flask_swagger_ui import get_swaggerui_blueprint
import os
import config


application = Flask(__name__)
application.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY  # os.environ['JWT_SECRET_KEY']
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60
application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
application.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
application.config['PROPAGATE_EXCEPTIONS'] = True

api = Api(application)

SWAGGER_URL = "/swagger"
API_URL_SWAG = "/static/swagger.yaml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL_SWAG,
    config={
        "app_name": "BOOKME"
    }
)

application.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
jwt = JWTManager(application)
try:
    DB.global_mongo_init(config.MONGO_HOST,  # os.environ['MONGO_HOST']
                         config.MONGO_DB_NAME)  # os.environ['MONGO_DB_NAME']
except Exception as e:
    print(f"Error: {e}")


# ======================================all-books====================================#

api.add_resource(Resources.BookCreateUpdateResource, '/book/', '/book', '/book/<book_id>/', '/book/<book_id>')
api.add_resource(Resources.AllBookResource, '/books/all/', '/books/all')

# ===============================User======================================= #

api.add_resource(Resources.UserRegister, '/user/register', '/user/register/')
api.add_resource(Resources.AllUserFetchResource, '/user/all', '/user/all/')
api.add_resource(Resources.Login, '/user', '/user/', '/user/login', '/user/login/')
api.add_resource(Resources.Logout, '/user/logout', '/user/logout/')
api.add_resource(Resources.UpdateUserDetails,
                 '/user/update/',
                 '/user/update',
                 '/user/<string:user_email>')
api.add_resource(Resources.UserEmailUpdateResource, '/user/update/email', '/user/update/email/')
api.add_resource(Resources.UserPasswordUpdateResource, '/user/update/password', '/user/update/password/')
api.add_resource(Resources.UserNameUpdateResource, '/user/update/username', '/user/update/username/')


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
        application.config['JWT_ERROR_MESSAGE_KEY']: 'Your session has expired. Please login again to continue.'
    }, 401


@jwt.expired_token_loader
def expired_token_check_callback():
    return {
        application.config['JWT_ERROR_MESSAGE_KEY']: 'Your session has expired. Please login again to continue.'
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
        application.config['JWT_ERROR_MESSAGE_KEY']: "{}.".format(error)
    }, 401


application.run(port=5000, debug=False)
