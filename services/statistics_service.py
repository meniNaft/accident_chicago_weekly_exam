from datetime import timedelta
from dateutil import parser
from dateutil.relativedelta import relativedelta
import repositories.accidents_repository as accidents_repo


def get_accidents_by_area_and_time(beat_id, time_type, str_date_time):
    if not time_type and not str_date_time:
        accidents_count = accidents_repo.get_accidents_by_area(beat_id)
        return {
            "beat_id": beat_id,
            "accidents_count": accidents_count
        }

    current_date_time = parser.parse(str_date_time)
    if time_type == 'day':
        start_date = current_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = current_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    elif time_type == 'week':
        start_date = current_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=6, hours=23, minutes=59, seconds=59, microseconds=999999)
    elif time_type == 'month':
        start_date = current_date_time.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end_date = (start_date + relativedelta(months=1)) - timedelta(seconds=1)
    else:
        return {"error": "Invalid time type"}, 400

    accidents_count = accidents_repo.get_accidents_by_area_and_time(beat_id, start_date, end_date)
    return {
        "beat_id": beat_id,
        "accidents_count": accidents_count,
        "time_type": time_type,
        "start_date": start_date.isoformat(),
        "end_date": end_date.isoformat()
    }


def get_accidents_by_cause(beat_id: int):
    return accidents_repo.get_accidents_by_cause(beat_id)


def get_injury_statistics_by_area(beat_id: int):
    res = accidents_repo.get_injury_statistics_by_area(beat_id)
    return res
