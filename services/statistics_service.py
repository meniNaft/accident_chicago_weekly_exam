import repositories.accidents_repository as accidents_repo


def get_accidents_by_area(beat_id: int):
    accidents_count = accidents_repo.get_accidents_by_area(beat_id)
    return {
        "beat_id": beat_id,
        "accidents_count": accidents_count
    }
