import Models
import time
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
    def find_by_name_author_genre(book):
        result_book = Models.Book.objects(name=book['name'], author=book['author'], genre=book['genre']).first()
        return result_book
