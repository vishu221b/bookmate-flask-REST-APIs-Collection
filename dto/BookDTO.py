def book_dto(book):
    try:
        if not book:
            return None
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
            'is_active': book.is_active,
            'privacy_scope': book.privacy_scope,
            'document_name': book.document_name,
            'entity_tag': book.entity_tag,
            'book_repo': book.repo_key
        }
    except Exception as e:
        print("DEBUG: Exception - {}, occurred at BOOK_DTO.".format(e))


def embed_book_dto(book):
    try:
        return {
            'id': str(book.pk),
            'book_name': book.name,
            'author': book.author,
            'summary': book.summary
        }
    except Exception as e:
        print("DEBUG: Exception - {}, occurred at EMBED_BOOK_DTO.".format(e))


def public_book_response_dto(book):
    try:
        if not book:
            return None
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
            'is_active': book.is_active,
            'privacy_scope': book.privacy_scope
        }
    except Exception as e:
        print("DEBUG: Exception - {}, occurred at PUBLIC_BOOK_RESPONSE_DTO.".format(e))
