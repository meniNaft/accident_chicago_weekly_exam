import repositories.accidents_repository as accidents_repo
from dateutil import parser


def test_get_all():
    res = accidents_repo.get_all()
    assert res


def test_get_accidents_by_area():
    res = accidents_repo.get_accidents_by_area(225)
    assert res


def test_get_accidents_by_area_and_time():
    current_date_time = parser.parse("9/05/2023")
    start_date = current_date_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = current_date_time.replace(hour=23, minute=59, second=59, microsecond=999999)
    print(start_date)
    print(end_date)
    accidents_count = accidents_repo.get_accidents_by_area_and_time(225, start_date, end_date)
    assert accidents_count


def test_get_accidents_by_cause():
    res = accidents_repo.get_accidents_by_cause(225)
    assert res


def test_get_injury_statistics_by_area():
    res = accidents_repo.get_injury_statistics_by_area(225)
    assert res
