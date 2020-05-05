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

    @staticmethod
    def delete_book(book_id, user_email):
        try:
            book = validate_for_deletion(book_id)
            if book['error']:
                return book['response'][0], book['response'][1]
            response = BookDAO.delete_book_by_id(book_id, user_email)
            verify_deleted_book = verify_delete(book_id)
            if verify_deleted_book:
                return response
            return {'error': 'There was some internal error, please contact the developer.'}, 500
        except Exception as e:
            print(e.__cause__)
            return {'error': e.args}


def verify_delete(book_id):
    fresh_book = BookDAO.find_active_inactive_book_by_id(book_id)
    if not fresh_book.is_active:
        return True
    return False


def validate_for_deletion(book_id):
    if len(book_id) != 24:
        return {'response': [{'error': 'Invalid length exception for book id = {}.'.format(book_id)}, 400],
                'error': True}
    if not BookDAO.find_active_inactive_book_by_id(book_id):
        return {'response': [{'error': 'No book exists for id {}'.format(book_id)}, 400],
                'error': True}
    book = verify_delete(book_id)
    if book:
        return {'response': [{'error': 'No book exists for the id {}.'.format(book_id)}, 400],
                'error': True}
    return {'error': False}


def check_if_book_already_exists(book):
    c_book = BookDAO.find_by_name_author_genre(book)
    if c_book:
        return True
    return False
