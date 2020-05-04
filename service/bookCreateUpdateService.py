from Dao.bookDAO import BookDAO


class BookCreateUpdateService:
    @staticmethod
    def create_new_book(new_book, created_by):
        validated_existence = check_if_book_already_exists(new_book)
        if validated_existence is True:
            return {'error': 'Book with the same name already exists for this author.'}, 409
        new_book['created_by'] = created_by
        new_book['last_updated_by'] = created_by
        return BookDAO.create_new_book(new_book)


def check_if_book_already_exists(book):
    c_book = BookDAO.find_by_name_author_genre(book)
    if c_book:
        return True
    return False
