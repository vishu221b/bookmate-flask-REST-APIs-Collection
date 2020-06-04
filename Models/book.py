import mongoengine as mon
import datetime


class Book(mon.Document):
    name = mon.StringField(required=True, max_length=255)
    summary = mon.StringField()
    author = mon.StringField(required=True)
    genre = mon.StringField(required=True)
    barcode = mon.StringField(max_length=20)
    created_at = mon.ComplexDateTimeField(default=datetime.datetime.now)
    created_by = mon.StringField(required=True)
    last_updated_at = mon.ComplexDateTimeField(default=datetime.datetime.now)
    last_updated_by = mon.StringField(required=False)
    is_active = mon.BooleanField(default=True)
    privacy_scope = mon.StringField(required=True, default="PUBLIC")
    book_cover_url = mon.URLField()
    document_name = mon.StringField()
    repo_key = mon.StringField()
    entity_tag = mon.StringField()

    meta = {
        'db_alias': 'bms_ent',
        'collection': 'books'
    }