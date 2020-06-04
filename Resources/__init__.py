from factories import BlueprintResourceFactory
from . import (users, books, admin)
from .users import *
from .books import *
from .admin import *
from .files import *


def generate_resources_for_app(app):
    resources = [users, books, admin]
    current_resources = BlueprintResourceFactory(app, resources)
    current_resources.create_blueprints()
