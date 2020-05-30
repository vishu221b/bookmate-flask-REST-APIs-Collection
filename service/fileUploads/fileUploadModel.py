from abc import ABC, abstractmethod
from mimetypes import guess_type
from werkzeug.utils import secure_filename


class FileUploadServiceBaseModel(ABC):

    @abstractmethod
    def upload_file(self):
        pass

    @abstractmethod
    def verify_file_extension(self, f_name):
        pass

    def get_mime_type(self, file_name):
        _type, _meta = guess_type(file_name)
        return str(_type)

    def get_secure_filename(self, file_name, _user_id, _file_extension):
        sec_name = secure_filename(file_name)
        if sec_name:
            return sec_name
        return f"{_user_id}_document.{_file_extension}"
