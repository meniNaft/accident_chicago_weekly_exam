from datetime import datetime

from config.db_connect import accidents


def get_all():
    return accidents.find().limit(100)


def get_accidents_by_area(beat_id: int):
    return accidents.count_documents({"beat_of_occurrence": beat_id})


def get_accidents_by_area_and_time(beat_id: int, start_date: datetime, end_date: datetime):
    return accidents.count_documents({
        "beat_of_occurrence": beat_id,
        "date.full_date": {
            "$gte": start_date.strftime("%m/%d/%Y %H:%M"),
            "$lte": end_date.strftime("%m/%d/%Y %H:%M")
        }
    })