import Models
import Utils.UserUtils as UserUtils
import time


class UserDAO:
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
    def get_favourite_books_by_email(email):
        books = []
        user = Models.User.objects(email=email)
        for i in user.fav_books:
            book = Models.Book.objects(_id=i).to_json()
            books.append(book)
        return books

    @staticmethod
    def create_user(user):
        new_user = Models.User()
        try:
            returned_user = UserUtils.validate_and_convert_new_user_request_object(user, new_user)
            if isinstance(returned_user, str):
                return {"error": returned_user}
            returned_user.save()
            return UserUtils.user_dto(returned_user)  # type is dictionary
        except Exception as e:
            return "[{}]".format(e)

    @staticmethod
    def update_user_generic_data(user_id, user):
        new_user = UserDAO.get_user_by_id(user_id)
        try:
            updated_user = UserUtils.convert_update_request_for_persistence(user, new_user)
            updated_user.save(force_insert=False)
            return UserUtils.user_dto(updated_user)
        except Exception as e:
            return "error: {}".format(e)

    @staticmethod
    def update_email(identity, new_em):
        user = UserDAO.get_user_by_id(identity)
        try:
            user.email = new_em
            user.save(force_insert=False)
            is_update_verified = verify_email_update_for_user(user, new_em)
            if not is_update_verified:
                return [{'error':'There was some error. Error Code: {}'.format(str(int(time.time()*1000)))}, 500]
            response = UserUtils.convert_user_dto_to_public_response_dto(UserUtils.user_dto(user))
            return [{'Success': 'Email updated successfully.', 'updatedUserDetails': response}, 200]
        except Exception as e:
            return [{"error": "There was some error. Exception: {}, Error Code: {}".format(e, str(int(time.time()*1000)))}, 500]

    @staticmethod
    def update_password(identity, opa, npa):
        user = UserDAO.get_user_by_id(identity)
        if user.password != opa:
            return [{'error': 'Invalid old Password. Please check your password and try again.'}, 403]
        user.password = npa
        user.save()
        verify_user = UserDAO.get_active_user_by_email(user.email)
        if verify_user.password == npa:
            return [{'Success': 'Password updated successfully for user.'}, 200]
        return [{'error': 'There was some error. Please retry again. Error code: {}'.format(str(int(time.time()*1000)))}, 500]

    @staticmethod
    def update_username(identity, new_username):
        user = UserDAO.get_user_by_id(identity)
        user.username = new_username
        user.save()
        user = UserUtils.user_dto(user)
        is_validated = verify_username_update_for_user(user, new_username)
        if is_validated:
            return [
                {
                    'Success': 'Username successfully updated.',
                    'updatedUserDetails': UserUtils.convert_user_dto_to_public_response_dto(user)
                }, 200
            ]
        return [{'Error': 'There was some error. Please retry again. Error code: {}'.format(str(int(time.time()*1000)))}, 500]

    @staticmethod
    def delete_user(user):
        user_instance = UserDAO.get_user_by_id(user['id'])
        user_instance.is_active = False
        user_instance.save()
        confirm_operation = UserDAO.get_active_inactive_single_user_by_email(user['id'])
        if confirm_operation and not confirm_operation.is_active:
            return True
        return False


def verify_username_update_for_user(user: dict, username: str) -> bool:
    if user['username'] == username:
        return True
    return False


def verify_if_username_already_exists(username):
    user = UserDAO.get_user_by_username(username)
    if not user:
        return False
    return True


def verify_email_update_for_user(user: dict, email: str) -> bool:
    if user['email'] == email:
        return True
    return False


def verify_if_email_already_exists(email):
    user = UserDAO.get_active_inactive_single_user_by_email(email)
    if not user:
        return False
    return True
