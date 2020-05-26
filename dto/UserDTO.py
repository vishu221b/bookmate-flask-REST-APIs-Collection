from Utils import UserUtils
from . import BookDTO
from . import EmbeddedDocumentDTO


def user_dto(user):
    try:
        book_bucket = list()
        books = UserUtils.get_user_favourite_books(user)
        if books:
            for book in books:
                book_bucket.append(BookDTO.embed_book_dto(book))
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
            'followers': [EmbeddedDocumentDTO.generate_embedded_dto(user) for user in list(user.all_followers)],
            'following': [EmbeddedDocumentDTO.generate_embedded_dto(user) for user in list(user.all_following)],
            'blocked': [EmbeddedDocumentDTO.generate_embedded_dto(user) for user in list(user.blocked_users)]
        }
    except Exception as e:
        print("DEBUG: Exception occurred at USER_DTO_PRIVATE - {}".format(e))
