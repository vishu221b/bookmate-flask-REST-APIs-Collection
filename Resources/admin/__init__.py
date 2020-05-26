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
                                         '/admin/user/delete/<user_email>',
                                         '/admin/user/delete/<user_email>/',
                                         '/admin/user/activate/<user_email>',
                                         '/admin/user/activate/<user_email>/',
                                         '/admin/privileges/<permission_type>/<user_email>',
                                         '/admin/privileges/<permission_type>/<user_email>/')
        resource.get('api').add_resource(AdminBookOperationsResource,
                                         '/admin/book/delete/<book_id>', '/admin/book/delete/<book_id>/',
                                         '/admin/book/restore/<book_id>', '/admin/book/restore/<book_id>/')
        resource.get('api').add_resource(SessionDetailsResource,
                                         '/admin/sessionDetails',
                                         '/admin/sessionDetails/')

    def _init_singleton_resource(self):
        self.blueprint_map = self._generate_api_blueprint()
        self._init_api_resources(self.blueprint_map)
        return self.blueprint_map
