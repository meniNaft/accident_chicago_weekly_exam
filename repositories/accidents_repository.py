from config.db_connect import accidents


def get_all():
    return accidents.find().limit(100)

