from Models.sessionHistory import SessionHistory
from Models.user import User
import datetime
from flask_jwt_extended import decode_token
from service.userCreateUpdateService import get_existing_user_by_id


class SessionHistoryDAO:
    def insert_login_session(self, email, access_token):
        session = SessionHistory()
        session.user_details = User.objects(email=email).first()
        session.access_token = access_token
        session.access_token_jti = str(decode_token(access_token)['jti'])
        session.save()

    def update_session(self, access_token_jti):
        session = SessionHistory.objects(access_token_jti=access_token_jti).first()
        if not session:
            print({'error': 'Not found'})
            return
        session.update(
            set__is_revoked=True,
            set__revoked_at=datetime.datetime.now())

    def get_session_details(self, token, is_admin):
        if is_admin:
            session = SessionHistory.objects(access_token=token).first()
            return session_dto(session)
        return False

    def get_revoked_tokens(self):
        token_bucket = SessionHistory.objects(is_revoked=True)
        return token_bucket


def session_dto(session):
    session_response = dict()
    session_response['id'] = str(session.pk)
    session_response['created_at'] = str(session.created_at)
    session_response['user_details'] = get_existing_user_by_id(session.user_details.id)
    session_response['access_token'] = str(session.access_token)
    session_response['access_token_jti'] = str(session.access_token_jti)
    session_response['revoked_at'] = str(session.revoked_at)
    session_response['is_revoked'] = str(session.is_revoked)
    return session_response
