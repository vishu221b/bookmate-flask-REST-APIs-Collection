from . import FileUploadServiceBaseModel
import io
from Utils import SecurityUtils
from Enums import BookEnums, ErrorEnums
from werkzeug.datastructures import FileStorage
from Dao.bookDAO import BookDAO
import datetime
from dto.BookDTO import book_dto


class DocumentUploadServiceImpl(FileUploadServiceBaseModel):

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
        response = self._aws_service.upload_file_to_s3(
            repoKey=self._repo_key,
            fileName=self._file_name,
            fileContent=self._file_obj,
            fileContentType=self.get_mime_type(self._file_name),
            contentACL='private'
        )
        return response

    def verify_file_extension(self, f_name: str):
        _file_extension = f_name.rsplit('.')[1]
        if _file_extension.lower() not in BookEnums.ALLOWED_EXTENSIONS.value:
            return [{'error': 'Please upload a file with valid file extension.'}, 403]
        return _file_extension

    def process_file_for_upload(self, _user_id: str, _book_id: str, f_obj: FileStorage, _privacy_scope: str):
        self._file_extension = self.verify_file_extension(f_obj.filename)
        if isinstance(self._file_extension, list):
            return self._file_extension
        self._book = BookDAO.find_active_book_by_id(_book_id)
        if not self._book:
            return [ErrorEnums.NO_BOOK_FOUND_ERROR.value, 404]
        if not self._book.is_active:
            return [ErrorEnums.INACTIVE_BOOK_ERROR.value, 400]
        self._privacy_scope = _privacy_scope.upper()
        if self._privacy_scope not in BookEnums.PRIVACY_SCOPES_FOR_DOCUMENT.value:
            return [{'error': 'Please provide a valid privacy type.'}, 400]
        self._user_id = _user_id
        self._file_stream = f_obj.read()
        self._file_obj = self.bytes_to_obj()
        self._file_name = self.get_secure_filename(f_obj.filename, self._user_id, self._file_extension)
        self._repo_key = self.make_repo_key()
        _upload_response = self.upload_file()
        response = self.update_file_record(_upload_response)
        if isinstance(response, list):
            return response
        return [{'response': {'updatedBookDetails': book_dto(response)}}, 200]

    def update_file_record(self, response):
        e_tag = response.get('ETag')
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
            self._book, self._repo_key, e_tag, self._file_name, self._privacy_scope)
        return response

    def bytes_to_obj(self):
        return self._stream_processor.BytesIO(self._file_stream)

    def make_repo_key(self):
        return SecurityUtils.calculate_md5(self._user_id)

    def download_file(self):
        pass
