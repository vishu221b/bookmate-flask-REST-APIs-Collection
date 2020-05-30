from flask_restful import (
    reqparse,
    Resource
)
from flask import request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from werkzeug.datastructures import FileStorage


class DocumentFileUploadResource(Resource):
    parser = reqparse.RequestParser().add_argument('documentFile', type=FileStorage, location='files')

    @jwt_required
    def post(self):
        _user = get_jwt_identity()
        _scope = request.args.get('privacyScope')
        _book_id = request.args.get('bookId')
        _raw_doc = DocumentFileUploadResource.parser.parse_args().get('documentFile')
        pass
