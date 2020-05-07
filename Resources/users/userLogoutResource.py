from flask_restful import Resource
from flask_jwt_extended import jwt_required


class Logout(Resource):
    @jwt_required
    def delete(self):
        pass
