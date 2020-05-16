def book_dto(book):
    try:
        return {
            'id': str(book.pk),
            'book_name': book.name,
            'summary': book.summary if book.summary else "",
            'author': book.author,
            'book_genre': book.genre,
            'barcode': book.barcode,
            'created_at': str(book.created_at),
            'created_by': book.created_by,
            'last_updated_at': str(book.last_updated_at),
            'last_updated_by': book.last_updated_by,
            'is_active': book.is_active
        }
    except Exception as e:
        print("Error at book_dto=>{}".format(e))
