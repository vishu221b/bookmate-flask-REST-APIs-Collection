from enum import Enum


class UserQueries(Enum):
    create_table = "CREATE TABLE if not exists user(" \
                   "id INTEGER PRIMARY KEY autoincrement," \
                   " first_name varchar not null," \
                   " last_name varchar," \
                   " email varchar unique not null," \
                   " username varchar not null," \
                   " password varchar not null," \
                   " created_at varchar not null," \
                   " last_updated_at varchar," \
                   " is_active int not null," \
                   " is_admin int not null)"
    new_user_insertion = "INSERT into user(first_name," \
                         " last_name," \
                         " email," \
                         " username," \
                         " password," \
                         " created_at," \
                         " last_updated_at," \
                         " is_active," \
                         " is_admin)" \
                         " VALUES" \
                         "(?,?,?,?,?,?,?,?,?)"

    fetch_user_id = "SELECT id, first_name, last_name, username, email, password, created_at, is_active," \
                    "is_admin, last_updated_at from user where id in (?)"

    fetch_user_name = "SELECT id, username, email, password, is_admin, is_active from user where username in (?)"

    fetch_user_email = "SELECT id, username, email, password, is_admin, is_active from user where email in (?)"

    fetch_all_users = "SELECT * from user"

    update_user = 'UPDATE user SET first_name=(?), ' \
                  'last_name=(?), ' \
                  'username=(?), ' \
                  'email=(?), ' \
                  'last_updated_at=(?), ' \
                  'is_active=(?), ' \
                  'is_admin=(?) ' \
                  'WHERE id=(?)'

    mark_is_active_false = "UPDATE user SET is_active=? WHERE id=?"
