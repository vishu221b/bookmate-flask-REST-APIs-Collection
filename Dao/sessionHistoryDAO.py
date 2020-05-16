from Models.sessionHistory import SessionHistory
from Models.user import User
import datetime
from flask_jwt_extended import decode_token
from dto import SessionDTO


class SessionHistoryDAO:

    def __init__(self):
        self.session = None
        self.token_bucket = None
        self.SessionNotFoundError = {'error': 'Not found.'}

    def insert_login_session(self, email, access_token):
        self.session = SessionHistory()
        self.session.user_details = User.objects(email=email).first()
        self.session.access_token = access_token
        self.session.access_token_jti = str(decode_token(access_token)['jti'])
        self.session.save()

    def update_session(self, access_token_jti):
        self.session = SessionHistory.objects(access_token_jti=access_token_jti).first()
        if not self.session:
            print(self.SessionNotFoundError)
            return
        self.session.update(
            set__is_revoked=True,
            set__revoked_at=datetime.datetime.now())

    def get_session_details(self, token):
        self.session = SessionHistory.objects(access_token=token).first()
        if self.session:
            return self.session
        return False

    def get_revoked_tokens(self):
        self.token_bucket = SessionHistory.objects(is_revoked=True)
        return self.token_bucket

    def get_active_sessions_for_user(self, user):
        self.token_bucket = list()
        sessions = SessionHistory.objects(user_details=user.get('id'), is_revoked=False).all()
        for session in sessions:
            session = SessionDTO.session_dto(session)
            self.token_bucket.append(session)
        return self.token_bucket if len(self.token_bucket) > 0 else None
