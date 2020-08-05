from flask import Flask
from flask_jwt_extended import JWTManager
from resources import *
import db
import routes
from flask_swagger_ui import get_swaggerui_blueprint
import projectSettings
from flask_cors import CORS


application = Flask(__name__)
CORS(application)
application.config['JWT_SECRET_KEY'] = projectSettings.JWT_SECRET_KEY
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60
application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']
application.config['JWT_ERROR_MESSAGE_KEY'] = 'error'
application.config['PROPAGATE_EXCEPTIONS'] = True

jwt = JWTManager(application)
db.initiate_mongo()
generate_resources_for_app(application)
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

application.run(port=5000)
