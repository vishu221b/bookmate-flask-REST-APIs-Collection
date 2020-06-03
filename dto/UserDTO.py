from Utils import UserUtils
from . import BookDTO
from . import EmbeddedDocumentDTO


def user_dto(user):
    try:
        if not user:
            print(f"DEBUG: Received : {user} for user_dto.")
            return None
        book_bucket = list()
        books = UserUtils.get_user_favourite_books(user)
        if books:
            for book in books:
                book_bucket.append(BookDTO.embed_book_dto(book))
        user_followers = [EmbeddedDocumentDTO.generate_embedded_dto(user) for user in list(user.all_followers)]
        user_following = [EmbeddedDocumentDTO.generate_embedded_dto(user) for user in list(user.all_following)]
        user_blocked = [EmbeddedDocumentDTO.generate_embedded_dto(user) for user in list(user.blocked_users)]
        return {
            'id': str(user.pk),
            'first_name': user.first_name,
            'last_name': user.last_name if user.last_name else "",
            'date_of_birth': str(user.date_of_birth)[:10],
            'email': user.email,
            'phone_number': user.phone_number,
            'username': user.username,
            'alternate_username': user.alt_username,
            'is_active': user.is_active,
            'created_at': str(user.created_at),
            'password': str(user.password),
            'is_admin': bool(user.is_admin),
            'fav_books': book_bucket if book_bucket else [],
            'followers': user_followers if user_followers else [],
            'following': user_following if user_following else [],
            'blocked': user_blocked if user_blocked else []
        }
    except Exception as e:
        print("DEBUG: Exception occurred at USER_DTO_PRIVATE - {}".format(e))
