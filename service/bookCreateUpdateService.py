from Dao.bookDAO import BookDAO
from dto.BookDTO import book_dto


class BookCreateUpdateService:
    def __init__(self):
        self.book = None

    @staticmethod
    def create_new_book(new_book, created_by_user):
        validated_existence = check_if_book_already_exists(new_book)
        code_check = check_if_bar_code_exists(new_book)
        if code_check['error']:
            return code_check['response'][0], code_check['response'][1]
        if validated_existence:
            return {'error': 'Book with the same name already exists for this author.'}, 409
        return BookDAO.create_new_book(new_book, created_by_user)

    @staticmethod
    def delete_book(book_id, user, is_admin_request: bool) -> list:
        try:
            valid_book = validate_for_deletion(book_id)
            if valid_book.get('error'):
                return valid_book.get('response')
            book = BookDAO.find_active_inactive_book_by_id(book_id)
            if is_admin_request or book.created_by == user.get('id'):
                response = BookDAO.delete_book_by_id(book_id, user.get('id'))
                verify_deleted_book = verify_delete(book_id)
                if verify_deleted_book:
                    return [response, 200]
                return [{'error': 'There was some error.'}, 500]
            return [{'error': 'Book can only be deleted by it\'s respective owner.'}, 403]
        except Exception as e:
            return [{'error': e.args}, 400]

    @staticmethod
    def get_books_for_user(user):
        books = BookDAO.find_by_created_by_user(user.get('id'))
        if books and len(books) > 0:
            return {'response': books}, 200
        return {'error': 'No books have been added yet.'}, 404

    @staticmethod
    def update_book(book: dict, updated_by: dict):
        try:
            c_book = validate_book_id(book.get('id'))
            if c_book.get('error'):
                return c_book.get('response')[0], c_book.get('response')[1]
            response = BookDAO.update_book_by_id(book, updated_by)
            return response
        except Exception as e:
            return {'error': e.args}, 500

    @staticmethod
    def restore_book(book_id, owner, is_admin_request: bool) -> list:
        validate = validate_book_id(book_id)
        if validate.get('error'):
            return validate.get('response')
        verify_status = verify_delete(book_id)
        if not verify_status:
            return [{'error': 'Book is already active.'}, 409]
        book = BookDAO.find_active_inactive_book_by_id(book_id)
        if is_admin_request or book.created_by == owner.get('id'):
            response = BookDAO.restore_inactive_book(book_id, owner.get('id'))
            return [response, 200]
        return [{'error': 'Books can be restored only by their respective owners.'}, 403]

    @staticmethod
    def get_all_books():
        all_books = BookDAO.find_all_active_books()
        response = []
        if not all_books:
            return {'error': 'No active books found in the repository.'}, 404
        for book in all_books:
            response.append(book_dto(book))
        return response, 200

    def get_active_book_by_id(self, book_id):
        valid_book = validate_book_id(book_id)
        if valid_book.get('error'):
            return valid_book.get('response')
        self.book = BookDAO.find_active_book_by_id(book_id)
        return self.book


def verify_delete(book_id):
    fresh_book = BookDAO.find_active_inactive_book_by_id(book_id)
    if not fresh_book.is_active:
        return True
    return False


def validate_for_deletion(book_id):
    book = validate_book_id(book_id)
    if book.get('error'):
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
    book = BookDAO.find_active_inactive_book_by_id(book_id)
    if not book:
        return {'response': [{'error': 'No book exists for id {}'.format(book_id)}, 400],
                'error': True}
    return {'error': False,  'book': book}


def check_if_bar_code_exists(book):
    code_book = BookDAO.get_by_barcode(book['barcode'])
    if code_book:
        return {
            'response': [{'error': 'Another book with the same barcode already exists. Please use a fresh barcode.'},
                         409],
            'error': True}
    return {'error': False}
