import mongoengine as meng
import datetime
from .book import Book


class User(meng.Document):
    created_at = meng.ComplexDateTimeField(default=datetime.datetime.now)
    first_name = meng.StringField(required=True, min_length=1, max_length=50)
    last_name = meng.StringField(required=False, max_length=50, default="")
    date_of_birth = meng.DateTimeField(required=True)
    phone_number = meng.LongField(required=True, max_value=99999999999)
    email = meng.EmailField(required=True, unique=True)
    username = meng.StringField(required=True, unique=True)
    password = meng.StringField(required=True)
    last_updated_at = meng.ComplexDateTimeField(default=datetime.datetime.now)
    is_admin = meng.BooleanField(default=False)
    is_active = meng.BooleanField(default=True)
    fav_books = meng.ListField(default=[])
    authored_books = meng.ListField(default=[])

    meta = {
        'db_alias': 'bms_ent',
        'collection': 'user'
    }