from Dao.sessionHistoryDAO import SessionHistoryDAO
from flask_jwt_extended import decode_token, create_access_token
from Utils.TimeUtils import TimeUtils
from dto.SessionDTO import session_dto
from Enums import SessionEnums, ErrorEnums
from Utils import UserUtils as UserConverter


class SessionService:

    def __init__(self):
        self.access_token = None
        self.session_dao = None

    def get_session_details_for_user(self, token, user, is_admin_request):
        try:
            decoded_token_details = decode_token(token, allow_expired=True)
            if not is_admin_request and user.get('id') != decoded_token_details.get('identity').get('id'):
                return [ErrorEnums.INVALID_TOKEN_EXCEPTION.value, 403]
            token_jti = decoded_token_details.get('jti')
            time = TimeUtils()
            self.session_dao = SessionHistoryDAO()
            session_details_bucket = self.session_dao.get_session_details(token_jti)
            if session_details_bucket:
                session_details_bucket = session_dto(session_details_bucket)
                session_details_bucket.setdefault(
                    'expiry',
                    str(time.format_epoch_to_date_time(decoded_token_details.get('exp')))
                )
                return [{
                            'response': session_details_bucket
                }, 200]
            return [{'error': ErrorEnums.SESSION_NOT_FOUND_ERROR.value}, 404]
        except Exception as e:
            return {'error': f'Exception {e} occurred, please contact developer.'}, 500

    def get_active_token_record(self, user):
        self.session_dao = SessionHistoryDAO()
        time_utils = TimeUtils()
        active_token_bucket = self.session_dao.get_active_sessions_for_user(user)
        if not active_token_bucket:
            return active_token_bucket
        for token in active_token_bucket:
            decoded_token = decode_token(token.get('access_token'), allow_expired=True)
            difference_delta = time_utils.calculate_difference_from_now((decoded_token.get('exp')) * 1000000)
            if difference_delta/(60*1000*1000) < SessionEnums.TOKEN_REVOKE_DELTA_IN_MINUTES.value:
                self.session_dao.update_session(token.get('access_token_jti'))
            else:
                self.access_token = token.get('access_token')
        return self.access_token

    def generate_fresh_session_token(self, user):
        session_token = create_access_token(identity=user)
        return session_token

    def revoke_session_token(self, jti):
        self.session_dao = SessionHistoryDAO()
        self.session_dao.update_session(jti)

    def generate_session_token(self, user):
        self.session_dao = SessionHistoryDAO()
        active_token = self.get_active_token_record(user)
        if active_token:
            return active_token
        session_token = self.generate_fresh_session_token(UserConverter.convert_user_dto_to_public_response_dto(user))
        self.session_dao.insert_login_session(user.get('email'), session_token)
        return session_token


def get_revoked_tokens():
    session_dao = SessionHistoryDAO()
    blacklisted_token_bucket = set()
    token_bucket = session_dao.get_revoked_tokens()
    for token in token_bucket:
        blacklisted_token_bucket.add(str(token.access_token_jti))
    return blacklisted_token_bucket


