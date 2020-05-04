from Dao.userDAO import UserDAO
from Utils import UserUtils as UserConverter, UserUtils, SecurityUtils


def confirm_if_username_or_email_exists_already_during_registration(user_email, user_name) -> dict:
    user_instance = UserDAO.get_active_inactive_single_user_by_email(user_email)
    user_email_already_exists_error = "Another user with the same email already exists."
    username_already_exists_error = "Another user with the same username already exists."
    if user_instance:
        return {'result': True, 'value': user_email_already_exists_error}
    else:
        username_instance = UserDAO.get_user_by_username(user_name)
        if username_instance:
            return {'result': True, 'value': username_already_exists_error}


def verify_id_email_for_email_update(uid, email):
    user = UserDAO.get_user_by_id(uid)
    if not user:
        return {'result': False, 'error': 'No user found with id {}.'.format(uid)}
    if isinstance(user, dict) and 'error' in user.keys():
        return user
    if user and user.email != email:
        return {'result': False, 'error': 'Mismatch in id and oldEmail. Please correct the pair and retry again.'}
    return True


def get_all_users() -> list:
    users_from_persistence = UserDAO.get_all_active_users()
    aggregated_result = []
    for user in users_from_persistence:
        aggregated_result.append(UserConverter.user_dto(user))
    return aggregated_result


def confirm_if_user_name_already_exists(username):
    user_instance = UserDAO.get_user_by_username(username)
    if user_instance.username == username:
        return True
    return False


def get_existing_user_by_username(username):
    user = UserDAO.get_user_by_username(username)
    return UserConverter.user_dto(user)


def get_existing_user_by_email(email):
    user = UserDAO.get_active_inactive_single_user_by_email(email)
    if not user:
        return {'error': 'No user found for email {}.'.format(email)}
    return UserConverter.user_dto(user)


def get_active_user_by_email(email):
    user = UserDAO.get_active_user_by_email(email)
    return UserConverter.user_dto(user)


def create_update_user(user_id, user, is_user_id_provided: bool):
    if not is_user_id_provided:
        created_user = UserDAO.create_user(user)
        return UserConverter.convert_user_dto_to_public_response_dto(created_user)
    updated_user = UserDAO.update_user_generic_data(user_id, user)
    return updated_user


def get_existing_user_by_id(identity) -> dict:
    user = UserDAO.get_user_by_id(identity)
    if isinstance(user, dict):
        return user
    return UserUtils.user_dto(user)


def update_user_email(user, old_em, new_em):
    is_length_valid = UserUtils.verify_email_length(old_em, new_em)
    if is_length_valid:
        return is_length_valid
    u = get_existing_user_by_id(user['id'])
    if 'error' in u.keys():
        return [u, 500]
    if u['email'] != old_em:
        return [{'error': '{} does not match your current email address. Please check and try again.'.format(old_em)}, 404]
    elif old_em == new_em:
        return [{'error': 'Email is already up to date for the user.'}, 200]
    email_exists_already = UserDAO.verify_if_email_already_exists(new_em)
    if email_exists_already:
        return [{'error': 'Cannot update email as the user with email id - {} already exists.'.format(new_em)}, 409]
    updated_user = UserDAO.update_email(user['id'], new_em)
    return updated_user


def delete_user(curr_user, email):
    is_length_valid = UserUtils.verify_email_length(email, email)
    if is_length_valid:
        return is_length_valid
    elif curr_user['email'] != email:
        return [{'error': 'Please provide a valid current email address.'}, 404]
    operation = UserDAO.delete_user(curr_user)
    if operation:  # # Active tokens for current user should be revoked as soon as the user marks himself as inactive.
        return [{'Success': operation}, 200]
    return [{'error': 'No active user found for email {}.'.format(email)}, 500]


def update_password(user, old_password, new_password):
    if not UserUtils.validate_length(
            old_password, 8) or not UserUtils.validate_length(new_password, 8):
        return [{'error': 'Please check the length of your input.',
                'help':
                    {
                        'oldPassword': 'Minimum length is 8.',
                        'newPassword': 'Minimum length is 8.'
                    }}, 404]
    persisted_p, requested_p = SecurityUtils.encrypt_pass(old_password), SecurityUtils.encrypt_pass(new_password)
    updated_user = UserDAO.update_password(user['id'], persisted_p, requested_p)
    return updated_user


def update_user_name(user: dict, old_username: str, new_username: str):
    is_length_verified = UserUtils.verify_username_length(old_username, new_username)
    if is_length_verified:
        return is_length_verified
    user = get_existing_user_by_id(user['id'])
    if 'error' in user.keys():
        return [user, 500]
    elif old_username != user['username']:
        return [
            {
                'Error': '{} does not match the current username. Please correct your username and retry again.'
                         .format(old_username)
            }, 404
        ]
    elif old_username == new_username:
        return [{'error': 'Username is already up to date for the user.'}, 200]
    if UserDAO.verify_if_username_already_exists(new_username):
        return [{'error': 'User with username - {} already exists.'.format(new_username)}, 409]
    response = UserDAO.update_username(user['id'], new_username)
    return response
