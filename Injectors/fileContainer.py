from dependency_injector import providers, containers
from service import DocumentUploadServiceImpl
from .AWSContainer import AWSContainer


class FileContainer(containers.DeclarativeContainer):
    document = providers.Factory(DocumentUploadServiceImpl, aws_serivce_instance=AWSContainer.aws_component)
