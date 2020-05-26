from factories import BlueprintFactory
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
        self.blueprint_factory = BlueprintFactory()
        self.blueprint_map = None

    def _generate_api_blueprint(self):
        return self.blueprint_factory.generate_fresh_blueprint('user', __name__)

    def _init_api_resources(self, resource):
        resource.get('api').add_resource(UserRegister, '/user/register', '/user/register/')
        resource.get('api').add_resource(AllUserFetchResource, '/user/all', '/user/all/')
        resource.get('api').add_resource(Login, '/user', '/user/', '/user/login', '/user/login/')
        resource.get('api').add_resource(Logout, '/user/logout', '/user/logout/')
        resource.get('api').add_resource(UpdateUserDetails,
                                         '/user/update/',
                                         '/user/update',
                                         '/user/<string:user_email>')
        resource.get('api').add_resource(UserEmailUpdateResource,
                                         '/user/update/email', '/user/update/email/')
        resource.get('api').add_resource(UserPasswordUpdateResource,
                                         '/user/update/password', '/user/update/password/')
        resource.get('api').add_resource(UserNameUpdateResource,
                                         '/user/update/username', '/user/update/username/')
        resource.get('api').add_resource(FollowUnfollowUsers,
                                         '/user/<user_to_be_followed_unfollowed>/<action>/fu',
                                         '/user/<user_to_be_followed_unfollowed>/<action>/fu/'
                                         )
        resource.get('api').add_resource(BlockUnblockUsers,
                                         '/user/<action>/<user_to_be_blocked_unblocked>',
                                         '/user/<action>/<user_to_be_blocked_unblocked>/')

    def _init_singleton_resource(self):
        self.blueprint_map = self._generate_api_blueprint()
        self._init_api_resources(self.blueprint_map)
        return self.blueprint_map
