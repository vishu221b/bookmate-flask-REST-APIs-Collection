from factories import BlueprintFactory
from .bookCreateUpdateResource import BookCreateUpdateResource
from .allBookResource import AllBookResource
from.markUnmarkFavourite import AddRemoveBookFromFavourites


class SingletonResourceFactory:
    def __init__(self):
        self.blueprint_factory = BlueprintFactory()
        self.blueprint_map = None

    def _generate_api_blueprint(self):
        return self.blueprint_factory.generate_fresh_blueprint('book', __name__)

    def _init_api_resources(self, resource):
        resource.get('api').add_resource(
            BookCreateUpdateResource, '/', '/<book_id>', '/<book_id>/')
        resource.get('api').add_resource(
            AllBookResource, '/fetch/all', '/fetch/all/')
        resource.get('api').add_resource(
            AddRemoveBookFromFavourites,
            '/favourite/<book_id>/<action>',
            '/favourite/<book_id>/<action>/')

    def _init_singleton_resource(self):
        self.blueprint_map = self._generate_api_blueprint()
        self._init_api_resources(self.blueprint_map)
        return self.blueprint_map
