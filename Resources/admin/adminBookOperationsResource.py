from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from service.bookCreateUpdateService import BookCreateUpdateService


class AdminBookOperationsResource(Resource):
    @jwt_required
    def delete(self, book_id):
        user = get_jwt_identity()
        if not user['is_admin']:
            return {'error': 'Only admins can access this resource.'}, 403
        response = BookCreateUpdateService.delete_book(book_id, user)
        return response

    @jwt_required
    def patch(self, book_id):
        try:
            user = get_jwt_identity()
            if not user['is_admin']:
                return {'error': 'Only admins can access this resource.'}, 403
            response = BookCreateUpdateService.restore_book(book_id, user)
            return response
        except Exception as e:
            return {'error': e.args}, 500
