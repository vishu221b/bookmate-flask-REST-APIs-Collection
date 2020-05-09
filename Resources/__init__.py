from .users import *
from .books import *
from .admin import *


def initiate_resources(api):
    # ======================================all-books====================================#

    api.add_resource(BookCreateUpdateResource, '/book', '/book/', '/book/<book_id>', '/book/<book_id>/')
    api.add_resource(AllBookResource, '/books/all', '/books/all/')

    # ===============================User======================================= #

    api.add_resource(UserRegister, '/user/register', '/user/register/')
    api.add_resource(AllUserFetchResource, '/user/all', '/user/all/')
    api.add_resource(Login, '/user', '/user/', '/user/login', '/user/login/')
    api.add_resource(Logout, '/user/logout', '/user/logout/')
    api.add_resource(UpdateUserDetails,
                     '/user/update/',
                     '/user/update',
                     '/user/<string:user_email>')
    api.add_resource(UserEmailUpdateResource, '/user/update/email', '/user/update/email/')
    api.add_resource(UserPasswordUpdateResource, '/user/update/password', '/user/update/password/')
    api.add_resource(UserNameUpdateResource, '/user/update/username', '/user/update/username/')

    # ===============================Admin===================================== #

    api.add_resource(AdminUserOperationsResource,
                     '/admin/user/delete/<user_email>',
                     '/admin/user/delete/<user_email>/')
    api.add_resource(AdminBookOperationsResource,
                     '/admin/book/delete/<book_id>', '/admin/book/delete/<book_id>/',
                     '/admin/book/restore/<book_id>', '/admin/book/restore/<book_id>/')
