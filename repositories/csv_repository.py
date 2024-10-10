import os
import csv
import datetime
from dotenv import load_dotenv
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
    print(datetime.datetime.now(), "start prepare data")
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
    print(datetime.datetime.now(), "total rows: ", len(data))

    data_chunks = [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]
    print(datetime.datetime.now(), "total chunks: ", len(data))

    print(datetime.datetime.now(), "start inserting data")
    for chunk in data_chunks:
        accidents.insert_many(chunk)
    print(datetime.datetime.now(), "end insert data")


def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


