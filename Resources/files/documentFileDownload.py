from flask_restful import reqparse, Resource
from flask_jwt_extended import jwt_required
from werkzeug import Response
from Injectors import FilesContainer


class DocumentFileDownloadResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('bookId', type=str, location='args')

    @jwt_required
    def get(self):
        try:
            _book_id = DocumentFileDownloadResource.parser.parse_args().get('bookId')
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
