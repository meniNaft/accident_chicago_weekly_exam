from config.db_connect import accidents


def get_all():
    return accidents.find().limit(100)


def get_accidents_by_area(beat_id: int):
    return accidents.count_documents({"beat_of_occurrence": beat_id})