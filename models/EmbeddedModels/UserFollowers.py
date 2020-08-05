import mongoengine as db
import datetime


class Followers(db.EmbeddedDocument):
    user_reference = db.StringField()
    user_email = db.EmailField()
    created_at = db.ComplexDateTimeField(default=datetime.datetime.now)
    last_updated_at = db.ComplexDateTimeField(default=datetime.datetime.now)
    is_active = db.BooleanField(default=True)
    version = db.IntField(default=0)
