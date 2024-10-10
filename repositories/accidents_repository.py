from datetime import datetime
from config.db_connect import accidents


def get_all():
    return accidents.find().limit(100)


def get_accidents_by_area(beat_id: int):
    return accidents.count_documents({"beat_of_occurrence": beat_id})


def get_accidents_by_area_and_time(beat_id: int, start_date: datetime, end_date: datetime):
    return accidents.count_documents({
        "beat_of_occurrence": beat_id,
        "full_date": {
            "$gte": start_date.strftime("%m/%d/%Y %H:%M"),
            "$lte": end_date.strftime("%m/%d/%Y %H:%M")
        }
    })


def get_accidents_by_cause(beat_id: int):
    pipeline = [
        {"$match": {"beat_of_occurrence": beat_id}},
        {"$group": {
            "_id": "$contributors.prim_contributory_cause",
            "count": {"$sum": 1}
        }},
        {"$project": {
            "cause": "$_id",
            "count": 1,
            "_id": 0
        }}
    ]

    results = accidents.aggregate(pipeline)
    return list(results)


def get_injury_statistics_by_area(beat_id: int):
    pipeline = [
        {"$match": {"beat_of_occurrence": beat_id}},
        {"$group": {
            "_id": None,
            "total_injuries": {"$sum": "$injuries.total"},
            "fatal_injuries": {"$sum": "$injuries.fatal"},
            "non_fatal_injuries": {
                "$sum": {
                    "$subtract": ["$injuries.total", "$injuries.fatal"]
                }
            },
            "events": {"$push": "$$ROOT"}
        }},
        {"$project": {
            "_id": 0,
            "total_injuries": 1,
            "fatal_injuries": 1,
            "non_fatal_injuries": 1,
            "events": 1
        }}
    ]

    result = list(accidents.aggregate(pipeline))
    return result[0] if result else {"total_injuries": 0, "fatal_injuries": 0, "non_fatal_injuries": 0, "events": []}
