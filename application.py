from flask import Flask, send_from_directory, redirect, url_for
from flask_restful import Api
import hashlib
from flask_jwt_extended import JWTManager
import Resources
import DB
from flask_swagger_ui import get_swaggerui_blueprint


application = Flask(__name__)
application.config['JWT_SECRET_KEY'] = hashlib.sha3_512("S3c|eT@K3Y".encode()).hexdigest()
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60
application.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(application)

SWAGGER_URL = "/def"
API_URL_SWAG = "/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL_SWAG,
    config={
        "app_name": "BUKME"
    }
)

application.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
jwt = JWTManager(application)
try:
    DB.global_mongo_init()
except Exception as e:
    print(f"Error: {e}")

# ======================================all-books====================================#

api.add_resource(Resources.BookCreateUpdateResource, '/book/', '/book', '/book/<book_id>/', '/book/<book_id>')
api.add_resource(Resources.AllBookResource, '/books/all/', '/books/all')

# ===============================User======================================= #

api.add_resource(Resources.UserRegister, '/user/register', '/user/register/')
api.add_resource(Resources.Login, '/user/login', '/user/login/')
api.add_resource(Resources.UpdateUserDetails,
                 '/user/update/details',
                 '/user/update/details/',
                 '/user/<string:user_email>')
api.add_resource(Resources.UserEmailUpdateResource, '/user/update/email', '/user/update/email/')
api.add_resource(Resources.UserPasswordUpdateResource, '/user/update/password', '/user/update/password/')
api.add_resource(Resources.UserNameUpdateResource, '/user/update/username', '/user/update/username/')


@application.route('/')
def index():
    return redirect('/def')


@application.route('/static/<path>')
def swag_route(path):
    return send_from_directory('static', path)
