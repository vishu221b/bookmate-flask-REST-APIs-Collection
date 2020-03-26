from enum import Enum


class BookQueries(Enum):
    create_book_table = "CREATE TABLE if not exists book(" \
                        "id INTEGER PRIMARY KEY AUTOINCREMENT," \
                        "name varchar not null," \
                        "author varchar," \
                        "description varchar" \
                        "created_by INTEGER not null," \
                        "last_updated_by INTEGER not null" \
                        "created_at varchar not null," \
                        "last_updated_at varchar," \
                        "FOREIGN KEY(created_by) REFERENCES user (id))," \
                        "FOREIGN KEY(last_updated_by) REFERENCES user (id))"
    create_book = ""
    new_book_insertion = ""
    fetch_book_by_id = ""
    fetch_book_by_name = ""
