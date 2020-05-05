from Dao.bookDAO import BookDAO
from Utils.BookUtils import book_dto


class BookCreateUpdateService:
    @staticmethod
    def create_new_book(new_book, created_by):
        validated_existence = check_if_book_already_exists(new_book)
        code_check = check_if_bar_code_exists(new_book)
        if code_check['error']:
            return code_check['response'][0], code_check['response'][1]
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
            return {'error': e.args}

    @staticmethod
    def get_books_for_user(user):
        books = BookDAO.find_by_created_by_user(user['email'])
        if books and len(books) > 0:
            return {'response': books}, 200
        return {'error': 'No books have been added yet.'}, 404

    @staticmethod
    def update_book(book):
        try:
            c_book = validate_book_id(book['id'])
            if c_book['error']:
                return c_book['response'][0], c_book['response'][1]
            response = BookDAO.update_book_by_id(book)
            return response
        except Exception as e:
            return {'error': e.args}, 500

    @staticmethod
    def restore_book(book_id, owner):
        validate = validate_book_id(book_id)
        if validate['error']:
            return validate['response'][0], validate['response'][1]
        verify_status = verify_delete(book_id)
        if not verify_status:
            return {'error': 'Book is already active.'}, 409
        book = BookDAO.find_active_inactive_book_by_id(book_id)
        if book.created_by == owner:
            response = BookDAO.restore_inactive_book(book_id)
            return response
        return {'error': 'Books can be restored only by their respective owners.'}, 403

    @staticmethod
    def get_all_books():
        all_books = BookDAO.find_all_active_books()
        response = []
        if not all_books:
            return {'error': 'No active books found in the repository.'}, 404
        for book in all_books:
            response.append(book_dto(book))
        return response, 200


def verify_delete(book_id):
    fresh_book = BookDAO.find_active_inactive_book_by_id(book_id)
    if not fresh_book.is_active:
        return True
    return False


def validate_for_deletion(book_id):
    book = validate_book_id(book_id)
    if book['error']:
        return book
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


def validate_book_id(book_id):
    if len(book_id) != 24:
        return {'response': [{'error': 'Invalid length exception for book id = {}.'.format(book_id)}, 400],
                'error': True}
    if not BookDAO.find_active_inactive_book_by_id(book_id):
        return {'response': [{'error': 'No book exists for id {}'.format(book_id)}, 400],
                'error': True}
    return {'error': False}


def check_if_bar_code_exists(book):
    code_book = BookDAO.get_by_barcode(book['barcode'])
    if code_book:
        return {
            'response': [{'error': 'Another book with the same barcode already exists. Please use a fresh barcode.'},
                         409],
            'error': True}
    return {'error': False}
