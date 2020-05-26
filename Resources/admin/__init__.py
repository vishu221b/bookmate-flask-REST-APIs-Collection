from factories import BlueprintFactory
from .adminBookOperationsResource import AdminBookOperationsResource
from .adminUserOperationsResource import AdminUserOperationsResource
from .getSessionDetailsResource import SessionDetailsResource


class SingletonResourceFactory:
    def __init__(self):
        self.blueprint_factory = BlueprintFactory()

    def _generate_api_blueprint(self):
        return self.blueprint_factory.generate_fresh_blueprint('admin', __name__)

    def _init_api_resources(self, resource):
        resource.get('api').add_resource(AdminUserOperationsResource,
                                         '/user/delete/<user_email>',
                                         '/user/delete/<user_email>/',
                                         '/user/activate/<user_email>',
                                         '/user/activate/<user_email>/',
                                         '/privileges/<permission_type>/<user_email>',
                                         '/privileges/<permission_type>/<user_email>/')
        resource.get('api').add_resource(AdminBookOperationsResource,
                                         '/book/delete/<book_id>', '/book/delete/<book_id>/',
                                         '/book/restore/<book_id>', '/book/restore/<book_id>/')
        resource.get('api').add_resource(SessionDetailsResource,
                                         '/sessionDetails',
                                         '/sessionDetails/')

    def _init_singleton_resource(self):
        self.blueprint_map = self._generate_api_blueprint()
        self._init_api_resources(self.blueprint_map)
        return self.blueprint_map
