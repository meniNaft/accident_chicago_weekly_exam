import csv
from config.db_connect import accidents
from dateutil import parser


def read_scv(csv_path: str):
    with open(csv_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            yield row


def init_accidents_db():
    accidents.drop()
    data = []
    date_format = '%m/%d/%Y %H:%M'
    for row in read_scv('./data/data_not_full.csv'):
        if len(data) > 0 and any(x for x in data if x["record_id"] == row['CRASH_RECORD_ID']):
            continue

        str_date_time = row['CRASH_DATE']
        current_date_time = parser.parse(str_date_time)
        new_accident = {
            'record_id': row['CRASH_RECORD_ID'],
            'date': {
                'full_date': str_date_time,
                'year': current_date_time.year,
                'month': current_date_time.month,
                'date': current_date_time.day
            },
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

    print("start inserting data")
    for chunk in data_chunks:
        accidents.insert_many(chunk)
    print("end insert data")


def safe_int(value, default=0):
    try:
        return int(value)
    except ValueError:
        return default


