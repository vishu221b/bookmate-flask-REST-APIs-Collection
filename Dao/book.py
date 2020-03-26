import time
import DB


class BookStore:
    def __int__(self, single_book):
        self.single_book = single_book

    def create_new_book(self):
        return {'bookCreationSuccessful': {'bookCreated': self}}, 201

    @staticmethod
    def update_existing_book():
        return

    @staticmethod
    def delete_book_by_id():
        return

    @staticmethod
    def get_book_by_id():
        return

    @staticmethod
    def get_book_by_name():
        return

    @staticmethod
    def get_all_books():
        return
