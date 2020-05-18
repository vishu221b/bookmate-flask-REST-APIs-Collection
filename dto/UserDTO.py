from . import UserUtils
from . import BookDTO


def user_dto(user):
    try:
        book_bucket = list()
        books = UserUtils.get_user_favourite_books(user)
        if books:
            for book in books:
                book_bucket.append(BookDTO.book_dto(book))
        return {
            'id': str(user.pk),
            'first_name': user.first_name,
            'last_name': user.last_name if user.last_name else "",
            'date_of_birth': str(user.date_of_birth)[:10],
            'email': user.email,
            'phone_number': user.phone_number,
            'username': user.username,
            'is_active': user.is_active,
            'created_at': str(user.created_at),
            'password': str(user.password),
            'is_admin': bool(user.is_admin),
            'fav_books': book_bucket if book_bucket else [],
        }
    except Exception as e:
        print("Error UDTO:2=>{}".format(e))
