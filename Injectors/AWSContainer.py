from service import AwsServiceBaseImpl
from dependency_injector import providers, containers


class AWSContainer(containers.DeclarativeContainer):
    aws_component = providers.Factory(AwsServiceBaseImpl)
