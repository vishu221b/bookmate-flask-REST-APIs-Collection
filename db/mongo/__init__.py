import mongoengine


def global_mongo_init(host, name):
    try:
        mongoengine.register_connection(
            alias='bms_ent',
            host=host,
            name=name)
    except Exception as e:
        print(e)


def mongo_disconnect():
    try:
        mongoengine.disconnect(alias='bms_ent')
    except Exception as e:
        print(e)
