import os
import csv
import datetime
from dotenv import load_dotenv
from pymongo import ASCENDING

from config.db_connect import accidents

load_dotenv()
csv_url = os.getenv("CSV_URL")


def read_scv(csv_path: str):
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def init_accidents_db():
    accidents.drop()
    data = []
    for row in read_scv(csv_url):
        if len(data) > 0 and any(x for x in data if x["record_id"] == row['CRASH_RECORD_ID']):
            continue

        new_accident = {
            'record_id': row['CRASH_RECORD_ID'],
            'full_date': row['CRASH_DATE'],
            'beat_of_occurrence': safe_int(row['BEAT_OF_OCCURRENCE']),
            'injuries': {
                'total': safe_int(row['INJURIES_TOTAL']),
                'fatal': safe_int(row['INJURIES_FATAL']),
                'incapacitating': safe_int(row['INJURIES_INCAPACITATING']),
                'non_incapacitating': safe_int(row['INJURIES_NON_INCAPACITATING']),
            },
            'contributors': {
                'prim_contributory_cause': row['PRIM_CONTRIBUTORY_CAUSE'],
                'sec_contributory_cause': row['SEC_CONTRIBUTORY_CAUSE'],
            }
        }
        data.append(new_accident)

    chunk_size = 100
    data_chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

    for chunk in data_chunks:
        accidents.insert_many(chunk)

    create_indexes()


def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


def create_indexes():
    # The following indexes are created to optimize performance based on the fields
    # most frequently used in the main queries, including filtering, aggregation, and
    # range queries:

    accidents.create_index([("beat_of_occurrence", ASCENDING)])
    accidents.create_index([("full_date", ASCENDING)])
    accidents.create_index([("contributors.prim_contributory_cause", ASCENDING)])
    accidents.create_index([("beat_of_occurrence", ASCENDING), ("full_date", ASCENDING)])

