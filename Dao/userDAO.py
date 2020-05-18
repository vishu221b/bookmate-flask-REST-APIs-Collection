import Models
import Utils.UserUtils as UserUtils
import time
import dto.UserDTO
from Enums import AdminPermissionEnums, UserEnums
import datetime


class UserDAO:

    def __init__(self):
        self.user = None
        self.book = None

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
            returned_user = UserUtils.validate_and_convert_new_user_request_object(user, new_user)
            if isinstance(returned_user, str):
                return {"error": returned_user}
            returned_user.save()
            return dto.UserDTO.user_dto(returned_user)  # type is dictionary
        except Exception as e:
            return "[{}]".format(e)

    @staticmethod
    def update_user_generic_data(user_identity, user):
        old_user = UserDAO.get_user_by_id(user_identity.get('id'))
        try:
            updated_user = UserUtils.convert_update_request_for_persistence(user, old_user)
            updated_user.last_updated_by = old_user
            updated_user.last_updated_at = datetime.datetime.now()
            updated_user.save(force_insert=False)
            return dto.UserDTO.user_dto(updated_user)
        except Exception as e:
            return "error: {}".format(e)

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
