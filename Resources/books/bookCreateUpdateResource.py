from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Constants import REQUEST_FIELDS_FOR_CREATION, REQUEST_FIELDS_FOR_UPDATE
from service.bookCreateUpdateService import BookCreateUpdateService
from Utils.BookUtils import validate_incoming_request_dto


class BookCreateUpdateResource(Resource):
    creation_parser = reqparse.RequestParser()
    for field in REQUEST_FIELDS_FOR_CREATION:
        creation_parser.add_argument(field)

    updation_parser = reqparse.RequestParser()
    for field in REQUEST_FIELDS_FOR_UPDATE:
        updation_parser.add_argument(field,
                                     required=True if field == "id" else False,
                                     help=f"{field} is a mandatory field.")

    @jwt_required
    def post(self):
        try:
            request = BookCreateUpdateResource.creation_parser.parse_args()
            validate = validate_incoming_request_dto(request)
            if not validate:
                user = get_jwt_identity()
                response = BookCreateUpdateService.create_new_book(request, user['email'])
                return response
            return validate
        except Exception as e:
            return {'error': e.args}, 500

    @jwt_required
    def get(self):
        try:
            response = BookCreateUpdateService.get_books_for_user(get_jwt_identity())
            return response
        except Exception as e:
            return {'error': e.args}, 500

    @jwt_required
    def put(self):
        request = BookCreateUpdateResource.updation_parser.parse_args()
        response = BookCreateUpdateService.update_book(request)
        return response

    @jwt_required
    def delete(self, book_id):
        user = get_jwt_identity()
        response = BookCreateUpdateService.delete_book(book_id, user['email'])
        return response

    @jwt_required
    def patch(self, book_id):
        try:
            user = get_jwt_identity()
            response = BookCreateUpdateService.restore_book(book_id, user['email'])
            return response
        except Exception as e:
            return {'error': e.args}, 500
