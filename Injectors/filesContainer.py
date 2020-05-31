from dependency_injector import providers, containers
from service import DocumentFileServiceBaseModelImpl
from .AWSContainer import AWSContainer


class FilesContainer(containers.DeclarativeContainer):
    document = providers.Factory(DocumentFileServiceBaseModelImpl, AWSContainer.aws_component)
