from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from Resources import *
import DB
import routes
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

#
# def init_blueprints(*args):
#     for arg in args:
#         if isinstance(arg, Blueprint):
#             application.register_blueprint(arg)


# # user = Blueprint('user', __name__, url_prefix="/user")
# book = Blueprint('book', __name__, url_prefix="/book")
# admin = Blueprint('admin', __name__, url_prefix="/admin")
#
# # user_api = Api(user)
# book_api = Api(book)
# admin_api = Api(admin)

jwt = JWTManager(application)
DB.initiate_mongo()
generate_all_resources_main(application)
routes.initiate_routes(application, jwt)

SWAGGER_URL = "/swagger"
API_URL_SWAG = "/static/swagger.yaml"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL_SWAG,
    config={
        "app_name": "BooKMate"
    }
)
application.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
application.run(port=5000, debug=True)
