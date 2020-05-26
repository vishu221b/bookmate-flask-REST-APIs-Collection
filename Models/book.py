import mongoengine as meng
import datetime


class Book(meng.Document):
    name = meng.StringField(required=True, max_length=255)
    summary = meng.StringField()
    author = meng.StringField(required=True)
    genre = meng.StringField(required=True)
    barcode = meng.StringField(max_length=20)
    created_at = meng.ComplexDateTimeField(default=datetime.datetime.now)
    created_by = meng.StringField(required=True)
    last_updated_at = meng.ComplexDateTimeField(default=datetime.datetime.now)
    last_updated_by = meng.StringField(required=False)
    is_active = meng.BooleanField(default=True)
    privacy_scope = meng.StringField(required=True, default="PUBLIC")
    book_cover_url = meng.URLField()
    book_url = meng.URLField()

    meta = {
        'db_alias': 'bms_ent',
        'collection': 'books'
    }