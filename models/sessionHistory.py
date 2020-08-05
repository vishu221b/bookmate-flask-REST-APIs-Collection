import mongoengine as me
import datetime
from . import User


class SessionHistory(me.Document):
    created_at = me.ComplexDateTimeField(default=datetime.datetime.now)
    user_details = me.ReferenceField(User, dbref=True)
    access_token = me.StringField()
    access_token_jti = me.StringField()
    revoked_at = me.ComplexDateTimeField(default=datetime.datetime.now)
    is_revoked = me.BooleanField(default=False)

    meta = {
        'db_alias': 'bms_ent',
        'collection': 'SessionHistory'
    }