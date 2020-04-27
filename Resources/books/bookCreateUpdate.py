from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from Constants import REQUEST_FIELDS_FOR_CREATE_UPDATE


class CreateUpdateBook(Resource):
    parser = reqparse.RequestParser()
    for field in REQUEST_FIELDS_FOR_CREATE_UPDATE:
        parser.add_argument(field,
                            required=True if field != "isActive" else False,
                            help="{} is missing from request.".format(field))

    @jwt_required
    def post(self):
        request = CreateUpdateBook.parser.parse_args()
        # Create book through Service
        return

    @jwt_required
    def get(self, book_id):
        # Get book through service
        return

    @jwt_required
    def put(self, book_id):
        request = reqparse.RequestParser().parse_args()
        # Update book through service
        return

    @jwt_required
    def delete(self, book_id):
        # Delete book through service
        return
