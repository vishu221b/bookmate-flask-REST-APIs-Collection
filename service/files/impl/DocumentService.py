from . import FileServiceBaseModel, bookCreateUpdateService
import io
from Utils import SecurityUtils, BookUtils
from Enums import BookEnums, ErrorEnums
from werkzeug.datastructures import FileStorage
from Dao.bookDAO import BookDAO
import datetime
from dto.BookDTO import book_dto


class DocumentFileServiceBaseModelImpl(FileServiceBaseModel):

    def __init__(self, aws_service_instance):
        self._aws_service = aws_service_instance
        self._book_dao = BookDAO()
        self._file_name = None
        self._file_obj = None
        self._file_stream = None
        self._file_extension = None
        self._stream_processor = io
        self._privacy_scope = None
        self._user_id = None
        self._book = None
        self._repo_key = None

    def upload_file(self):
        return self._aws_service.upload_file_to_s3(
            repoKey=self._repo_key,
            fileName=self._file_name,
            fileContent=self._file_obj,
            fileContentType=self.get_mime_type(self._file_name),
            contentACL=BookEnums.PRIVACY_SCOPES_FOR_DOCUMENT.value.get(self._privacy_scope)
        )

    def verify_file_extension(self, f_name: str):
        _file_extension = f_name.rsplit('.')[1]
        if _file_extension.lower() not in BookEnums.ALLOWED_EXTENSIONS.value:
            return [{'error': 'Please upload a file with valid file extension.'}, 403]
        return _file_extension

    def process_file_for_upload(self, _user_id: str, _book_id: str, f_obj: FileStorage, _privacy_scope: str):
        print(f"INFO: user: {_user_id} for book: {_book_id} for file: {f_obj} and privacy: {_privacy_scope}")
        self._file_extension = self.verify_file_extension(f_obj.filename)
        if isinstance(self._file_extension, list):
            return self._file_extension
        self._file_stream = f_obj.read()
        _file_size_in_mb = BookUtils.convert_bytes_to_mb(self._get_file_size())
        if _file_size_in_mb > BookEnums.MAX_FILE_SIZE_ALLOWED_IN_MB_FOR_DOC.value:
            return [ErrorEnums.MAX_SIZE_EXCEED_ERROR_FOR_DOC.value, 413]
        self._book = BookDAO.find_active_book_by_id(_book_id)
        if not self._book:
            return [ErrorEnums.NO_BOOK_FOUND_ERROR.value, 404]
        if self._book.created_by != _user_id:
            return [ErrorEnums.BOOK_OWNER_NOT_MATCH_ERROR.value, 404]
        if not self._book:
            return [ErrorEnums.NO_BOOK_FOUND_ERROR.value, 404]
        if not self._book.is_active:
            return [ErrorEnums.INACTIVE_BOOK_ERROR.value, 400]
        self._privacy_scope = _privacy_scope.upper()
        if self._privacy_scope not in BookEnums.PRIVACY_SCOPES_FOR_DOCUMENT.value:
            return [{'error': 'Please provide a valid privacy type.'}, 400]
        self._user_id = _user_id
        self._file_obj = self.bytes_to_obj()
        self._file_name = self.get_secure_filename(f_obj.filename, self._user_id, self._file_extension)
        self._repo_key = self.make_repo_key()
        _upload_response = self.upload_file()
        response = self.update_file_record(_upload_response)
        if isinstance(response, list):
            return response
        return [{'response': {'updatedBookDetails': book_dto(response)}}, 200]

    def update_file_record(self, response):
        e_tag = response.get('ETag')[1:-1]
        if not e_tag:
            print(
                "{}: DEBUG: Response received is - {}, for file {} and book id {}.".format(
                    str(datetime.datetime.now()),
                    str(response),
                    self._file_name,
                    self._book
                ))
            return [{'error': 'There was some error.'}, 500]
        response = self._book_dao.update_document_details_for_book(
            self._book, self._repo_key, e_tag, self._file_name, self._privacy_scope, self._user_id)
        return response

    def _get_file_size(self):
        return len(self._file_stream)

    def bytes_to_obj(self):
        return self._stream_processor.BytesIO(self._file_stream)

    def make_repo_key(self):
        return SecurityUtils.calculate_md5(self._user_id)

    def download_file(self, book_id):
        print("INFO: Received download request for book id {}".format(book_id))
        valid_book = bookCreateUpdateService.validate_book_id(book_id)
        if valid_book.get('error'):
            return valid_book.get('response')
        book = book_dto(valid_book.get('book'))
        if not book.get('is_active'):
            return [ErrorEnums.INACTIVE_BOOK_ERROR.value, 400]
        if book.get('privacy_scope') == BookEnums.PRIVATE.value:
            return [ErrorEnums.PROTECTED_BOOK_ACCESS_ERROR.value, 403]
        if not book.get('book_repo'):
            return [ErrorEnums.NO_BOOK_FOUND_ERROR.value, 404]
        response = self._aws_service.get_file_from_s3(
            repoKey=book.get('book_repo'),
            fileName=book.get('document_name'),
            eTag=book.get('entity_tag')
        )
        response.setdefault('file_name', book.get('document_name'))
        print(f"DEBUG: Final response for file download: {response}")
        return response
