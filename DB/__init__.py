from DB.mongo import global_mongo_init, mongo_disconnect
import os
import config


def initiate_mongo():
    try:
        global_mongo_init(config.MONGO_HOST,  # os.environ['MONGO_HOST'],
                          config.MONGO_DB_NAME)  # os.environ['MONGO_DB_NAME'])
    except Exception as e:
        print(f"Error: {e}")