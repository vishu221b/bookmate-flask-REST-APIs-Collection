from factories import ViewFactory
from .adminBookOperationsResource import AdminBookOperationsResource
from .adminUserOperationsResource import AdminUserOperationsResource
from .getSessionDetailsAdminResource import AdminSessionDetailsResource


class SingletonResourceFactory:
    def __init__(self):
        self.blueprint_factory = ViewFactory()

    def _generate_api_blueprint(self):
        return self.blueprint_factory.generate_fresh_blueprint('admin', __name__)

    def _init_api_resources(self, resource):
        resource.get('api').add_resource(AdminUserOperationsResource,
                                         '/user/mark/<action>/<user_email>',
                                         '/user/mark/<action>/<user_email>/',
                                         '/privileges/<permission_type>/<user_email>',
                                         '/privileges/<permission_type>/<user_email>/')
        resource.get('api').add_resource(AdminBookOperationsResource,
                                         '/book/delete/<book_id>', '/book/delete/<book_id>/',
                                         '/book/restore/<book_id>', '/book/restore/<book_id>/')
        resource.get('api').add_resource(AdminSessionDetailsResource,
                                         '/session/details',
                                         '/session/details/')

    def _init_singleton_resource(self):
        self.blueprint_map = self._generate_api_blueprint()
        self._init_api_resources(self.blueprint_map)
        return self.blueprint_map
