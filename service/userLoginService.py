import dto.UserDTO
from Dao.userDAO import UserDAO
import Utils.SecurityUtils as EncryptPass


def get_by_username(username):
    user = UserDAO.get_user_by_username(username)
    if user and not user.is_active and user.marked_active_inactive_by_admin:
        return "User is currently inactive. Please contact admin."
    user_dto = dto.UserDTO.user_dto(user)
    return user_dto


def get_by_email(email):
    user = UserDAO.get_active_inactive_single_user_by_email(email)
    if not user:
        return "No user found with email - {}.".format(email)
    if user and not user.is_active and user.marked_active_inactive_by_admin:
        return "User is currently inactive. Please contact admin"
    user_dto = dto.UserDTO.user_dto(user)
    return user_dto


def get_active_inactive_users_by_email(email):
    user_hold = UserDAO.get_active_inactive_single_user_by_email(email)
    return dto.UserDTO.user_dto(user_hold)


def convert_password(p) -> str:
    p = EncryptPass.encrypt_pass(p)
    return str(p)
