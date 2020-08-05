from db.mongo import global_mongo_init, mongo_disconnect
import projectSettings


def initiate_mongo():
    try:
        global_mongo_init(
            projectSettings.MONGO_HOST,
            projectSettings.MONGO_DB_NAME
    )
    except Exception as e:
        print(f"Error: {e}")