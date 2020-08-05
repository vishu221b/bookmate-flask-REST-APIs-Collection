from databaseService.userDatabaseService import UserDatabaseService
from enums import ErrorEnums, UserEnums
from dto.UserDTO import user_dto


class UserSocialService:
    def __init__(self):
        self.user = None
        self.target_user = None
        self.user_followers = []
        self.user_following = []
        self.blocked_users = []
        self.user_dao = None
        self._performer = None

    def follow_unfollow_a_user(
            self, requesting_user_email: str, user_to_be_followed_unfollowed_email: str, action) -> list:
        try:
            if requesting_user_email == user_to_be_followed_unfollowed_email:
                return [{'error': ErrorEnums.INVALID_INPUT_SUPPLIED_ERROR.value}, 400]
            self.target_user = UserDatabaseService.get_active_inactive_single_user_by_email(user_to_be_followed_unfollowed_email)
            if not self.target_user:
                return [{'error': ErrorEnums.NO_USER_FOUND_ERROR.value}, 404]
            if not self.target_user.is_active:
                return [{'error': ErrorEnums.INACTIVE_USER_ERROR.value}, 404]
            if action not in [UserEnums.FOLLOW.value, UserEnums.UNFOLLOW.value]:
                return [{'error': ErrorEnums.UNKNOWN_REQUEST_ERROR.value}, 400]
            self._performer = UserDatabaseService.get_active_user_by_email(requesting_user_email)
            self.user_dao = UserDatabaseService()
            response = self.user_dao.follow_unfollow_user(user_dto(self._performer), user_dto(self.target_user), action)
            if isinstance(response, dict):
                return [response, 500]
            return [{'response': 'SUCCESS.'}, 200]
        except Exception as e:
            return [{'error': 'Exception - {} - occurred.'.format(e)}, 400]

    def block_unblock_a_user(
            self, requestor_users_email: str, user_to_be_blocked_unblocked_email: str, action) -> list:
        try:
            if requestor_users_email == user_to_be_blocked_unblocked_email:
                return [{'error': ErrorEnums.INVALID_INPUT_SUPPLIED_ERROR.value}, 400]
            self.target_user = UserDatabaseService.get_active_inactive_single_user_by_email(user_to_be_blocked_unblocked_email)
            if not self.target_user:
                return [{'error': ErrorEnums.NO_USER_FOUND_ERROR.value}, 404]
            if not self.target_user.is_active:
                return [{'error': ErrorEnums.INACTIVE_USER_ERROR.value}, 404]
            if action not in [str(UserEnums.BLOCK.value), str(UserEnums.UNBLOCK.value)]:
                return [{'error': ErrorEnums.UNKNOWN_REQUEST_ERROR.value}, 400]
            self._performer = UserDatabaseService.get_active_user_by_email(requestor_users_email)
            self.user_dao = UserDatabaseService()
            self.user_dao.block_unblock_users(user_dto(self._performer), user_dto(self.target_user), action)
            return [{'response': 'SUCCESS.'}, 200]
        except Exception as e:
            return [{'error': ErrorEnums.EXCEPTION_ERROR.value.format(e, "block/unblock user request")}, 400]
