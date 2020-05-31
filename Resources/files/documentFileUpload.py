from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.datastructures import FileStorage
from werkzeug import Response
from Injectors import FilesContainer


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
            response = FilesContainer.document().process_file_for_upload(
                _user.get('id'),
                _book_id,
                _raw_doc,
                _scope
            )
            return response[0], response[1]
        except Exception as e:
            print(f"DEBUG: Received Exception : {e}")
            return {'exception': e.args}

    @jwt_required
    def get(self):
        try:
            _book_id = DocumentFileUploadResource.parser.parse_args().get('bookId')
            _book_resp = FilesContainer.document().download_file(_book_id)
            if isinstance(_book_resp, dict):
                response = Response(
                    _book_resp.get('Body').read(),
                    mimetype=_book_resp.get('ContentType'),
                    headers={'Content-Disposition': f"attachment;filename={_book_resp.get('file_name')}"}
                )
                print(f"DEBUG: Response headers for download request : {response.headers}")
                return response
            return _book_resp[0], _book_resp[1]
        except Exception as e:
            print(f"DEBUG: Exception - {e}, , occurred at GET DocumentFileUploadResource.")
            return {'exception': e.args}
