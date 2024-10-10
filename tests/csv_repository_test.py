from repositories.csv_repository import init_accidents_db
import repositories.accidents_repository as accidents_repo


def test_load_csv():
    init_accidents_db()
    res = accidents_repo.get_all()
    assert res
