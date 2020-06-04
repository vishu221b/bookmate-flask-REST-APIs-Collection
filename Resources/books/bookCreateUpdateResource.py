from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from Constants import REQUEST_FIELDS_FOR_CREATION, FIELDS_FOR_BOOK_UPDATE_REQUEST
from service.bookCreateUpdateService import BookCreateUpdateService
from Utils.BookUtils import validate_incoming_request_dto


class BookCreateUpdateResource(Resource):
    creation_parser = reqparse.RequestParser()
    for field in REQUEST_FIELDS_FOR_CREATION:
        creation_parser.add_argument(field)

    updation_parser = reqparse.RequestParser()
    for field in FIELDS_FOR_BOOK_UPDATE_REQUEST:
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
                response = BookCreateUpdateService.create_new_book(request, user)
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
        try:
            user = get_jwt_identity()
            request = BookCreateUpdateResource.updation_parser.parse_args()
            response = BookCreateUpdateService.update_book(request, user)
            return response
        except Exception as e:
            return {'error': 'Exception - {} - occurred.'.format(e.args)}, 400
