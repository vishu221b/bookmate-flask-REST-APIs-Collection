from abc import ABC, abstractmethod


class AwsServiceBase(ABC):

    @abstractmethod
    def get_session(self):
        pass

    @abstractmethod
    def get_aws_resource(self, resource):
        pass

    @abstractmethod
    def upload_file_to_s3(self, **params):
        pass

    @abstractmethod
    def get_file_from_s3(self, **params):
        pass

    @abstractmethod
    def replace_file_in_s3(self, repo_key, old_file, new_file):
        pass
