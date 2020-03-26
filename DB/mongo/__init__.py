import mongoengine


def global_mongo_init():
    try:
        mongoengine.register_connection(
            alias='bms_ent',
            host='mongodb+srv://prod_point:toor@mongo221-bb6hj.mongodb.net',
            name='bookmanagementsystem')

    except Exception as e:
        print("Couldn't connect to online, hence trying to connect locally. Error:{}".format(e))
        try:
            mongoengine.register_connection(alias='bms_ent', host='mongodb://localhost:27017/bookmanagementsystem')
        except Exception as e:
            print(e)


def mongo_disconnect():
    try:
        mongoengine.disconnect(alias='bms_ent')
    except Exception as e:
        print(e)
