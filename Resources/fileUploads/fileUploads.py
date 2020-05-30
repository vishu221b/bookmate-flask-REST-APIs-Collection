from flask_restful import reqparse, Resource
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from Injectors import FileContainer


class DocumentFileUploadResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('documentFile', type=FileStorage, location='files')
    parser.add_argument('privacyScope', type=str, location='args')
    parser.add_argument('bookId', type=str, location='args')

    @jwt_required
    def post(self):
        try:
            _user = get_jwt_identity()
            req = DocumentFileUploadResource.parser.parse_args()
            _scope = req.get('privacyScope')
            _book_id = req.get('bookId')
            _raw_doc = req.get('documentFile')
            response = FileContainer.document().process_file_for_upload(
                _user.get('id'),
                _book_id,
                _raw_doc,
                _scope
            )
            return response[0], response[1]
        except Exception as e:
            print(f"DEBUG: Received Exception : {e}")
            return {'exception': e.args}
