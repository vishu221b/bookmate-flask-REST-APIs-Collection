from factories import ViewFactory
from .userBlockUnblockResource import BlockUnblockUsers
from .userFollowUnfollowResource import FollowUnfollowUsers
from .userRegistrationResource import UserRegister
from .userEmailUpdateResource import UserEmailUpdateResource
from .userNameUpdateResource import UserNameUpdateResource
from .userPasswordUpdateResource import UserPasswordUpdateResource
from .userDetailsUpdateResource import UpdateUserDetails
from .userLoginResource import Login
from.userLogoutResource import Logout
from.allUserFetchResource import AllUserFetchResource


class SingletonResourceFactory:
    def __init__(self):
        self.blueprint_factory = ViewFactory()
        self.blueprint_map = None

    def _generate_api_blueprint(self):
        return self.blueprint_factory.generate_fresh_blueprint('user', __name__)

    def _init_api_resources(self, resource):
        resource.get('api').add_resource(UserRegister, '/register', '/register/')
        resource.get('api').add_resource(AllUserFetchResource, '/fetch/all', '/fetch/all/')  # TODO: Get user by id
        resource.get('api').add_resource(Login, '/', '/login', '/login/')
        resource.get('api').add_resource(Logout, '/logout', '/logout/')
        resource.get('api').add_resource(UpdateUserDetails,
                                         '/update/',
                                         '/update',
                                         '/<string:user_email>')
        resource.get('api').add_resource(UserEmailUpdateResource,
                                         '/update/email', '/update/email/')
        resource.get('api').add_resource(UserPasswordUpdateResource,
                                         '/update/password', '/update/password/')
        resource.get('api').add_resource(UserNameUpdateResource,
                                         '/update/username', '/update/username/')
        resource.get('api').add_resource(FollowUnfollowUsers,
                                         '/social/<action>/<user_to_be_followed_unfollowed>',
                                         '/social/<action>/<user_to_be_followed_unfollowed>/'
                                         )
        resource.get('api').add_resource(BlockUnblockUsers,
                                         '/perform/<action>/<user_to_be_blocked_unblocked>',
                                         '/perform/<action>/<user_to_be_blocked_unblocked>/')

    def _init_singleton_resource(self):
        self.blueprint_map = self._generate_api_blueprint()
        self._init_api_resources(self.blueprint_map)
        return self.blueprint_map
