import Models
import Models.EmbeddedModels as Embedded
import Utils.UserUtils as UserUtils
import time
import dto.UserDTO
from Enums import AdminPermissionEnums, UserEnums
import datetime
from CustomExceptions import UserException


class UserDAO:

    def __init__(self):
        self.is_follower_up_to_date = False
        self.is_following_up_to_date = False
        self.user = None
        self.book = None
        self.target_user = None
        self.followers, self.following, self.blocked_users = None, None, None

    @staticmethod
    def get_all_active_users():
        users = Models.User.objects(is_active=True).all()
        return users

    @staticmethod
    def get_all_inactive_users():
        users = Models.User.objects(is_active=False)
        return users

    @staticmethod
    def get_all_users():
        users = Models.User.objects()
        return users
# #----------------------------Email------------------------------------------

    @staticmethod
    def get_active_inactive_single_user_by_email(email):
        user_instance = Models.User.objects(email=email).first()
        return user_instance

    @staticmethod
    def get_active_user_by_email(email):
        user_instance = Models.User.objects(email=email, is_active=True).first()
        return user_instance
# #----------------------------Username----------------------------------------

    @staticmethod
    def get_active_user_by_username(username):
        user_instance = Models.User.objects(username=username, is_active=True).first()
        return user_instance

    @staticmethod
    def get_user_by_username(username):
        user_instance = Models.User.objects(username=username).first()
        return user_instance

    @staticmethod
    def get_user_by_alt_username(alt_username):
        user = Models.User.objects(alt_username=alt_username).first()
        return user
# #----------------------------------------------------------------------------

    @staticmethod
    def get_user_by_id(uid):
        try:
            user_instance = Models.User.objects(pk=str(uid)).first()
            return user_instance
        except Exception as e:
            return {'error': 'There was some error. Error code: {}'.format(str(int(time.time()*1000)))}

    @staticmethod
    def get_favourite_books_ids_by_email(email):
        books = []
        user = Models.User.objects(email=email).first()
        for i in user.fav_books:
            books.append(str(i.id))
        return books

    @staticmethod
    def create_user(user):
        new_user = Models.User()
        try:
            verify_alt_username_existence_for_email = UserDAO().get_user_by_alt_username(
                user.get('email').rsplit('@')[0]
            )
            returned_user = UserUtils.validate_and_convert_new_user_request_object(user, new_user)
            if isinstance(returned_user, str):
                return returned_user
            if verify_alt_username_existence_for_email:
                returned_user.alt_username = returned_user.username
            else:
                returned_user.alt_username = str(user.get('email').rsplit('@')[0])
            returned_user.save()
            return returned_user  # type is object
        except Exception as e:
            return "[{}]".format(e)

    @staticmethod
    def update_user_generic_data(user_identity, new_user_data):
        old_user_data = UserDAO.get_user_by_id(user_identity.get('id'))
        verify_alt_username_existence_for_email = UserDAO().get_user_by_alt_username(
            new_user_data.get('email').rsplit('@')[0]
        )
        try:
            updated_user = UserUtils.convert_update_request_for_persistence(new_user_data, old_user_data)
            updated_user.last_updated_at = datetime.datetime.now()
            updated_user.last_updated_by = old_user_data
            if verify_alt_username_existence_for_email:
                updated_user.alt_username = updated_user.username
            updated_user.save(force_insert=False)
            return old_user_data.reload()
        except Exception as e:
            return "{}".format(e)

    @staticmethod
    def update_email(identity, new_em):
        user = UserDAO.get_user_by_id(identity.get('id'))
        try:
            user.update(
                set__email=new_em,
                set__last_updated_at=datetime.datetime.now(),
                set__last_updated_by=user  # UserDAO.get_user_by_id(identity.get('id'))
            )
            updated_user = dto.UserDTO.user_dto(UserDAO.get_user_by_id(identity.get('id')))
            is_update_verified = verify_email_update_for_user(updated_user, new_em)
            if not is_update_verified:
                return [
                    {
                        'error': 'There was some error while updating email. Error Code: {}'.format(
                            str(int(time.time()*1000))
                        )
                    }, 500]
            response = UserUtils.convert_user_dto_to_public_response_dto(updated_user)
            return [{'Success': 'Email updated successfully.', 'updatedUserDetails': response}, 200]
        except Exception as e:
            return [
                {
                    "error": "There was some error. Exception: {}, Error Code: {}".format(
                        e, str(int(time.time()*1000))
                    )
                }, 500]

    @staticmethod
    def update_password(identity, opa, npa):
        user = UserDAO.get_user_by_id(identity.get('id'))
        if user.password != opa:
            return [{'error': 'Invalid old Password. Please check your password and try again.'}, 403]
        user.update(
            set__password=npa,
            set__last_updated_at=datetime.datetime.now(),
            set__last_updated_by=user
        )
        verify_user = UserDAO.get_active_user_by_email(user.email)
        if verify_user.password == npa:
            return [
                {
                    'Success':
                        'Password updated successfully for user.'
                }, 200
            ]
        return [
            {
                'error':
                    'There was some error. Please retry again. Error code: {}'.format(
                        str(int(time.time()*1000))
                    )
            }, 500
        ]

    @staticmethod
    def update_username(identity, new_username):
        user = UserDAO.get_user_by_id(identity.get('id'))
        user.update(
            set__username=new_username,
            set__last_updated_at=datetime.datetime.now(),
            set__last_updated_by=user
        )
        updated_user = dto.UserDTO.user_dto(UserDAO.get_user_by_id(identity.get('id')))
        is_validated = verify_username_update_for_user(updated_user, new_username)
        if is_validated:
            return [
                {
                    'Success': 'Username successfully updated.',
                    'updatedUserDetails': UserUtils.convert_user_dto_to_public_response_dto(updated_user)
                }, 200
            ]
        return [{'Error': 'There was some error. Please retry again. Error code: {}'.format(str(int(time.time()*1000)))}, 500]

    @staticmethod
    def activate_deactivate_user(performer, target_email, is_admin_action, action):
        user_instance = UserDAO.get_active_inactive_single_user_by_email(target_email)
        if user_instance:
            if action == AdminPermissionEnums.DEACTIVATE.name:
                user_instance.update(
                    set__marked_active_inactive_by_admin=is_admin_action,
                    set__is_active=AdminPermissionEnums.DEACTIVATE.value,
                    set__last_updated_at=datetime.datetime.now(),
                    set__last_updated_by=UserDAO.get_active_user_by_email(performer.get('email'))
                )
            elif action == AdminPermissionEnums.ACTIVATE.name:
                user_instance.update(
                    set__marked_active_inactive_by_admin=is_admin_action,
                    set__is_active=AdminPermissionEnums.ACTIVATE.value,
                    set__last_updated_at=datetime.datetime.now(),
                    set__last_updated_by=UserDAO.get_active_user_by_email(performer.get('email'))
                )

    @staticmethod
    def admin_access(performer, user_email, give_permission):
        user = Models.User.objects(email=user_email).first()
        user.update(
            set__is_admin=give_permission,
            set__last_updated_by=UserDAO.get_active_user_by_email(performer.get('email')),
            set__last_updated_at=datetime.datetime.now()
        )

    def set_unset_book_as_favourite(self, user, book, action):
        self.book = book
        self.user = UserDAO.get_active_user_by_email(user.get('email'))
        if action == UserEnums.MARK.name:
            self.user.update(
                push__fav_books=book,
                set__last_updated_by=UserDAO.get_active_user_by_email(user.get('email')),
                set__last_updated_at=datetime.datetime.now()
            )
        if action == UserEnums.REMOVE.name:
            self.user.update(
                pull__fav_books=book,
                set__last_updated_by=UserDAO.get_active_user_by_email(user.get('email')),
                set__last_updated_at=datetime.datetime.now()
            )

    def follow_unfollow_user(self, performer_user: dict, user_to_be_followed_unfollowed: dict, action: str):
        """

        :param performer_user: The user who has submitted the follow request
        :param user_to_be_followed_unfollowed: The user who will be followed
        :param action: Enum confirming if it is a Follow request or Unfollow request
        :return: None
        """
        self.user = UserDAO.get_active_user_by_email(performer_user.get('email'))
        self.target_user = UserDAO.get_active_user_by_email(user_to_be_followed_unfollowed.get('email'))

        follow_request = action == UserEnums.FOLLOW.value  # returns a boolean

        if self.target_user.all_followers and self.user.all_following:

            follower_in_target_user = self.target_user.all_followers.filter(user_reference=str(self.user.pk))

            following_in_performer_user = self.user.all_following.filter(user_reference=str(self.target_user.pk))

            ver1 = follower_in_target_user and not following_in_performer_user
            ver2 = following_in_performer_user and not follower_in_target_user

            if ver1 or ver2:
                print(
                    "DEBUG: Both the people must be in each other's records simultaneously! A mismatch is encountered."
                )
                # TODO: Manage response for this use case when there is a mismatch in records for whatever reason

            newer_version_for_the_one_being_followed = follower_in_target_user.first().version + 1

            follower_in_target_user.update(
                user_email=performer_user.get('email'),
                is_active=True if follow_request else False,
                last_updated_at=datetime.datetime.now(),
                version=newer_version_for_the_one_being_followed
            )
            self.target_user.save()
            self.is_follower_up_to_date = True

            newer_version_for_the_one_following = following_in_performer_user.first().version + 1

            following_in_performer_user.update(
                user_email=user_to_be_followed_unfollowed.get('email'),
                is_active=True if follow_request else False,
                last_updated_at=datetime.datetime.now(),
                version=newer_version_for_the_one_following
            )

            self.user.save()
            self.is_following_up_to_date = True

        if self.is_follower_up_to_date and self.is_following_up_to_date:
            return

        user_to_be_added_in_followers_list_of_target = Embedded.Followers(
            user_reference=str(self.user.pk),
            last_updated_at=datetime.datetime.now(),
            user_email=performer_user.get('email')
        )
        user_to_be_added_in_following_list_of_performer = Embedded.Following(
            user_reference=str(self.target_user.pk),
            last_updated_at=datetime.datetime.now(),
            user_email=user_to_be_followed_unfollowed.get('email')
        )
        self.target_user.update(
            push__all_followers=user_to_be_added_in_followers_list_of_target,
        )
        self.user.update(
            push__all_following=user_to_be_added_in_following_list_of_performer,
        )

    def block_unblock_users(self, performer: dict, user_to_be_blocked_unblocked: dict, action: str):
        self.user = UserDAO.get_active_user_by_email(performer.get('email'))
        self.target_user = UserDAO.get_active_user_by_email(user_to_be_blocked_unblocked.get('email'))

        block_user_request = action == UserEnums.BLOCK.value
        unblock_user_request = action == UserEnums.UNBLOCK.value

        if self.user.blocked_users:
            user_blocked_before = self.user.blocked_users.filter(user_reference=str(self.target_user.pk))
            if unblock_user_request and not user_blocked_before:
                raise UserException("Cannot unblock user as the user is not blocked yet")
            elif user_blocked_before:
                updated_version = user_blocked_before.first().version + 1
                user_blocked_before.update(
                    user_email=user_to_be_blocked_unblocked.get('email'),
                    is_active=True if block_user_request else False,
                    last_updated_at=datetime.datetime.now(),
                    version=updated_version
                )
                self.user.save()
                return

        if unblock_user_request:
            raise UserException("Cannot unblock user as the user is not blocked yet")

        user_to_be_added_to_blocked_records = Embedded.Blocked(
            user_reference=str(self.target_user.pk),
            last_updated_at=datetime.datetime.now(),
            user_email=user_to_be_blocked_unblocked.get('email')
        )

        self.user.update(
            push__blocked_users=user_to_be_added_to_blocked_records
        )

    def get_all_followers(self, user_email):
        self.followers = Models.User.objects(email=user_email).only('all_followers')
        if self.followers:
            return list(self.followers)
        return None

    def get_all_following(self, user_email):
        self.following = Models.User.objects(email=user_email).only('all_following')
        if self.following:
            return list(self.following)
        return None

    def get_blocked_users(self, user_email):
        self.blocked_users = Models.User.objects(email=user_email).only('blocked_users')
        if self.blocked_users:
            return list(self.blocked_users)
        return None


def verify_username_update_for_user(user: dict, username: str) -> bool:
    if user.get('username') == username:
        return True
    return False


def verify_if_username_already_exists(username):
    user = UserDAO.get_user_by_username(username)
    if not user:
        return False
    return True


def verify_email_update_for_user(user: dict, email: str) -> bool:
    if user.get('email') == email:
        return True
    return False


def verify_if_email_already_exists(email):
    user = UserDAO.get_active_inactive_single_user_by_email(email)
    if not user:
        return False
    return True
