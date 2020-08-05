from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.bookCreateUpdateService import BookCreateUpdateService
from enums import BookEnums


class BookDeleteRestoreResource(Resource):
    @jwt_required
    def post(self, book_id, action):
        try:
            user = get_jwt_identity()
            if action.upper() == BookEnums.RESTORE.name:
                response = BookCreateUpdateService.restore_book(book_id, user, False)
            elif action.upper() == BookEnums.DELETE.name:
                response = BookCreateUpdateService.delete_book(book_id, user, False)
            else:
                response = [{'error': 'There was some error'}, 400]
            return response[0], response[1]
        except Exception as e:
            return {'error': e.args}, 500
