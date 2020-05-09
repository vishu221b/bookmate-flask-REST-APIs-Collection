from DB.mongo import global_mongo_init, mongo_disconnect
import os


def initiate_mongo():
    try:
        global_mongo_init(os.environ['MONGO_HOST'],
                          os.environ['MONGO_DB_NAME']
    except Exception as e:
        print(f"Error: {e}")