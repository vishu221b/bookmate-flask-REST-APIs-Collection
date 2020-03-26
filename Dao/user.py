import time
import DB

con_cursor = DB.init_con_cur()
con_cursor[1].execute(DB.UserQueries.create_table.value)
con_cursor[1].close()


class User:
    def __init__(self):
        self.name = None

    @staticmethod
    def create_new_user(user_data):
        if User.get_user_by_email(user_data['email']):
            return {'errorMessage': 'User with the same email already exists.'}, 409
        con_cur = DB.init_con_cur()
        con_cur[1].execute(DB.UserQueries.new_user_insertion.value, (user_data['firstName'],
                                                                     user_data['lastName'],
                                                                     user_data['email'],
                                                                     user_data['username'],
                                                                     user_data['password'],
                                                                     str(int(time.time() * 1000)),
                                                                     None,
                                                                     1,
                                                                     user_data['isAdmin']
                                                                     ))
        con_cur[0].commit()
        con_cur[0].close()
        user_by_email = User.get_user_by_email(user_data['email'])
        return {'successMessage': user_by_email}

    @staticmethod
    def get_user_by_id(uid):
        con_cur = DB.init_con_cur()
        row = con_cur[1].execute(DB.UserQueries.fetch_user_id.value, (uid,)).fetchone()
        if row:
            response = {'userId': row[0],
                        'firstName': row[1],
                        'lastName': row[2],
                        'userName': row[3],
                        'email': row[4],
                        'password': row[5],
                        'createdAt': row[6],
                        'isActive': row[7],
                        'isAdmin': row[8],
                        'lastUpdatedAt': row[9]
                        }
        else:
            response = None
        con_cur[0].close()
        return response

    @staticmethod
    def get_user_by_email(email):
        con_cur = DB.init_con_cur()
        for i in con_cur[1].execute(DB.UserQueries.fetch_user_email.value, (email,)):
            if i:
                response = {'userId': i[0],
                            'username': i[1],
                            'email': i[2],
                            'password': 'mD5' + i[3] + '2==',
                            'isAdmin': i[4],
                            'isActive': i[5]}
            else:
                response = None
            con_cur[0].close()
            return response

    @staticmethod
    def get_user_by_username(username):
        con_cur = DB.init_con_cur()
        res = con_cur[1].execute(DB.UserQueries.fetch_user_name.value, (username,))
        row = res.fetchone()
        if row:
            user = {'userId': row[0],
                    'username': row[1],
                    'email': row[2],
                    'password': row[3],
                    'isAdmin': row[4],
                    'isActive': row[5]
                    }
        else:
            user = None
        con_cur[0].close()
        return user

    @staticmethod
    def update_user(user):
        con_cur = DB.init_con_cur()
        con_cur[1].execute(DB.UserQueries.update_user.value,
                           (user['firstName'],
                            user['lastName'],
                            user['username'],
                            user['email'],
                            str(int(time.time() * 1000)),
                            user['isActive'],
                            user['isAdmin'],
                            user['id']))
        con_cur[0].commit()
        con_cur[0].close()
        updated_user = User.get_user_by_id(user['id'])
        return updated_user

    @staticmethod
    def delete_user(user_id):
        con_cur = DB.init_con_cur()
        rex = con_cur[1].execute(DB.UserQueries.mark_is_active_false.value, (0, user_id))
        con_cur[0].commit()
        con_cur[0].close()
        inactive_user = User.get_user_by_id(user_id)
        if inactive_user and inactive_user['isActive'] == 0:
            return {'response': 'User has been marked as INACTIVE in the system.'}, 200
        return {'errorMessage': inactive_user}


