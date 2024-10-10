import services.statistics_service as statistics_service


def test_get_accidents_by_area_and_time():
    res = statistics_service.get_accidents_by_area_and_time(225, 'day', "9/05/2023")
    assert res


def test_get_accidents_by_cause():
    res = statistics_service.get_accidents_by_cause(225)
    assert res


def test_get_injury_statistics_by_area():
    res = statistics_service.get_injury_statistics_by_area(225)
    assert res
