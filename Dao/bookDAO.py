import Models
import datetime
from Utils import BookUtils


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
