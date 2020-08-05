from flask_restful import Resource
from service.bookCreateUpdateService import BookCreateUpdateService
from flask_jwt_extended import jwt_required


class AllBookResource(Resource):
    @jwt_required
    def get(self):
        try:
            response = BookCreateUpdateService.get_all_books()
            return response
        except Exception as e:
            return {'error': e.args}, 500

    @jwt_required
    def post(self):
        return {'error': 'Method not allowed.'}, 405

    @jwt_required
    def put(self):
        return {'error': 'Method not allowed.'}, 405

    @jwt_required
    def delete(self):
        return {'error': 'Method not allowed.'}, 405
