from abc import ABC, abstractmethod


class FileUpload(ABC):
    @abstractmethod
    def upload_file(self):
        pass
