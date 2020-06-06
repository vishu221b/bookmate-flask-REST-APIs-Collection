try:
    from config import (
        MONGO_DB_NAME, MONGO_HOST, AWS_BUCKET, AWS_KEY_SECRET, AWS_KEY_ID, JWT_SECRET_KEY
    )
except ModuleNotFoundError as e:
    print('INFO: Reached import under PROJECT SETTINGS, going live....')
    import os
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME')
    MONGO_HOST = os.environ.get('MONGO_HOST')
    AWS_BUCKET = os.environ.get('AWS_BUCKET')
    AWS_KEY_SECRET = os.environ.get('AWS_KEY_SECRET')
    AWS_KEY_ID = os.environ.get('AWS_KEY_ID')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
