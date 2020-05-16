from service import userCreateUpdateService
from Utils.UserUtils import convert_user_dto_to_public_response_dto


def session_dto(session):
    session_response = dict()
    session_response.setdefault('id', str(session.pk))
    session_response.setdefault('created_at', str(session.created_at))
    session_response.setdefault(
        'user_details',
        convert_user_dto_to_public_response_dto(
            userCreateUpdateService.get_existing_user_by_id(
                session.user_details.id
            )
        )
    )
    session_response.setdefault('access_token', str(session.access_token))
    session_response.setdefault('access_token_jti', str(session.access_token_jti))
    session_response.setdefault('is_revoked', str(session.is_revoked))
    session_response.setdefault('revoked_at', str(session.revoked_at))
    return session_response
