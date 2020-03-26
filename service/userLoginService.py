from Dao.userDAO import UserDAO
from flask_jwt_extended import create_access_token
import Utils.SecurityUtils as EncryptPass
import Utils.UserUtils as UserConverter


def get_by_username(username):
    user_hold = UserDAO.get_user_by_username(username)
    if user_hold and not user_hold.is_active:
        return "User is currently inactive."
    user_hold_dto = UserConverter.user_dto(user_hold)
    return user_hold_dto  # create separate for login purpose with password field


def get_by_email(email):
    user_hold = UserDAO.get_active_inactive_single_user_by_email(email)
    if not user_hold:
        return "No user found with email - {}.".format(email)
    if user_hold and not user_hold.is_active:
        return "User is currently inactive."
    final_use = UserConverter.user_dto(user_hold)
    return final_use


def get_active_inactive_users_by_email(email):
    user_hold = UserDAO.get_active_inactive_single_user_by_email(email)
    return UserConverter.user_dto(user_hold)


def generate_session_token(user):
    user_session_token = create_access_token(identity=user)
    return user_session_token


def convert_password(p) -> str:
    p = EncryptPass.encrypt_pass(p)
    return str(p)
