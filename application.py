from flask import Flask
from flask_restful import Api
import hashlib
from flask_jwt_extended import JWTManager, jwt_required
import Resources
import DB


application = Flask(__name__)
application.config['JWT_SECRET_KEY'] = hashlib.sha3_512("S3c|eT@K3Y".encode()).hexdigest()
application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 60 * 60
application.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(application)
jwt = JWTManager(application)
try:
    DB.global_mongo_init()
except Exception as e:
    print(f"Error: {e}")

# ======================================all-books====================================#

# api.add_resource(Resources.Books, '/books/', '/books')
# api.add_resource(Resources.Book, '/book/', '/book', '/book/<int:b_id>')

# ===============================User======================================= #

api.add_resource(Resources.UserRegister, '/', '/user/register', '/user/register/')
api.add_resource(Resources.Login, '/user/login', '/user/login/')
api.add_resource(Resources.UpdateUserDetails, '/user/update/details', '/user/update/details/', '/user/<string:user_email>')
api.add_resource(Resources.UserEmailUpdateResource, '/user/update/email', '/user/update/email/')
api.add_resource(Resources.UserPasswordUpdateResource, '/user/update/password', '/user/update/password/')
api.add_resource(Resources.UserNameUpdateResource, '/user/update/username', '/user/update/username/')


if __name__ == "__main__":
    try:
        application.run(host='0.0.0.0', port=8080, debug=False)
    except Exception as e:
        print("Then this happened->{}".format(e))
