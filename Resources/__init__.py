from factories import ResourceFactory
from . import (users, books, admin)
from .users import *
from .books import *
from .admin import *


def generate_resources_for_app(app):
    resources = [users, books, admin]
    current_resources = ResourceFactory(app, resources)
    print(current_resources.resource_blueprints)
    current_resources.create_blueprints()
