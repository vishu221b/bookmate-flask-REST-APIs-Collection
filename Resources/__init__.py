from factories import ResourceFactory
from . import (users, books, admin)
from .users import *
from .books import *
from .admin import *


def generate_all_resources_main(app):
    all_resources = [users, books, admin]
    resources = ResourceFactory(app, all_resources)
    print(resources.resource_blueprints)
    resources.create_blueprints()
