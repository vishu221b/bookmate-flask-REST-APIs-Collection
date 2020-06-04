from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_raw_jwt
from service import userCreateUpdateService


class AddRemoveBookFromFavourites(Resource):
    @jwt_required
    def post(self, book_id, action: str):
        try:
            user = get_jwt_identity()
            user.setdefault('_session_signature', get_raw_jwt().get('jti'))
            response = userCreateUpdateService.mark_unmark_book_as_favourite(
                user, book_id, action.upper()
            )
            return response[0], response[1]
        except Exception as e:
            print('DEBUG: Exception - {}, occurred while adding book as favourite.'.format(e))
            return {'error': e.args}, 400

    @jwt_required
    def delete(self, book_id, action: str):
        try:
            user = get_jwt_identity()
            user.setdefault('_session_signature', get_raw_jwt().get('jti'))
            response = userCreateUpdateService.mark_unmark_book_as_favourite(
                user, book_id, action.upper()
            )
            return response[0], response[1]
        except Exception as e:
            print('DEBUG: Exception - {}, occurred while removing book as favourite.'.format(e))
            return {'error': e.args}, 400
