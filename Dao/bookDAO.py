import Models
import datetime
from Utils import BookUtils
from Constants.BookConstants import REQUEST_FIELDS_FOR_UPDATE


class BookDAO:
    @staticmethod
    def create_new_book(book_dto):
        book = Models.Book()
        try:
            new_book = BookUtils.convert_new_book_request_object_for_persistence(book_dto, book)
            if isinstance(new_book, str):
                return {'error': new_book}, 404
            new_book.save()
            return {'response': BookUtils.book_dto(new_book)}, 201
        except Exception as e:
            return {'error': f"Exception, {e}, occurred."}, 500

    @staticmethod
    def delete_book_by_id(book_id, user_email):
        book = Models.Book.objects(pk=str(book_id)).first()
        if book.created_by == user_email:
            book.is_active = False
            book.last_updated_at = datetime.datetime.now()
            book.save()
            return {'response': 'Book was successfully removed.'}, 200
        return {'response': 'Book can only be deleted by it\'s owner.'}, 403

    @staticmethod
    def update_book_by_id(req_book):
        book = BookDAO.find_active_inactive_book_by_id(req_book['id'])
        if not book.is_active:
            return {'error': 'Cannot update an inactive book. Please restore the book to active first.'}, 403
        up_book = BookUtils.book_dto(book)
        for field in REQUEST_FIELDS_FOR_UPDATE:
            if field != "id" and req_book[field] and len(req_book[field].strip()) > 0:
                up_book[field] = req_book[field]
        validated_existence = BookDAO.find_by_name_author_genre(up_book)
        book_by_barcode = BookDAO.get_by_barcode(up_book['barcode'])
        if validated_existence and BookUtils.book_dto(validated_existence)['id'] != req_book['id']:
            return {'error': 'Book with the same name already exists for this author.'}, 409
        if up_book['barcode']\
                and len(up_book['barcode'].strip()) > 1\
                and book_by_barcode and BookUtils.book_dto(book_by_barcode)['id'] != req_book['id']:
            return {'error': 'Another book with the same barcode already exists. Please use a fresh barcode.'}, 409
        book.name = up_book['name']
        book.summary = up_book['summary']
        book.genre = up_book['genre']
        book.barcode = up_book['barcode']
        book.author = up_book['author']
        book.last_updated_at = datetime.datetime.now()
        book.save()
        response = {
                       'response': {
                           'Success': 'Book Sucessfully updated.',
                           'updated_book': BookUtils.book_dto(book)
                       }
                   }, 200
        return response

    @staticmethod
    def restore_inactive_book(book_id):
        try:
            book = Models.Book.objects(pk=str(book_id)).first()
            book.is_active = True
            book.last_updated_at = datetime.datetime.now()
            book.save()
            return {'response': 'Book was successfully restored.'}, 200
        except Exception as e:
            return {'error': e.args}, 500

    @staticmethod
    def find_by_created_by_user(email):
        all_books = []
        books = Models.Book.objects(created_by=email)
        for book in books:
            all_books.append(BookUtils.book_dto(book))
        return all_books

    @staticmethod
    def find_all_active_books():
        books = Models.Book.objects(is_active=True)
        return books

    @staticmethod
    def find_book_by_author(author):
        books = Models.Book.objects(author=author)
        return books

    @staticmethod
    def find_by_name_author_genre(book):
        result_book = Models.Book.objects(name=book['name'], author=book['author'], genre=book['genre']).first()
        return result_book

    @staticmethod
    def find_active_inactive_book_by_id(book_id):
        book = Models.Book.objects(pk=str(book_id)).first()
        return book

    @staticmethod
    def get_by_barcode(barcode):
        book = Models.Book.objects(barcode=barcode).first()
        return book
