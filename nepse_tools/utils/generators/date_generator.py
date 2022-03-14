import datetime
from typing import Generator


def date_range(
        start: str | datetime.date,
        end: str | datetime.date = datetime.datetime.now().date()
) -> Generator[datetime.date, None, None]:
    """
    Generates range of `datetime.date` objects from start to end.

    Args:
        start: Date starts from
        end: Date ends one day before

    Returns:
        Generates list of `datetime.date` objects between given dates

    """

    start_datetime = start
    end_datetime = end
    time_delta = datetime.timedelta(days=1)

    if type(start) is str:
        start_datetime = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    if type(end) is str:
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    while start_datetime < end_datetime:
        start_datetime += time_delta
        yield start_datetime
