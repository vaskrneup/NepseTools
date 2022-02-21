import datetime


class SharePrice:
    def __init__(
            self, start_datetime: datetime.datetime, end_datetime: datetime.datetime,
            opening_price: float, closing_price: float,
            high_price: float, low_price: float,
            volume: int, turnover: float, transactions: int,
            difference: float
    ):
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.opening_price = opening_price
        self.closing_price = closing_price
        self.high_price = high_price
        self.low_price = low_price
        self.volume = volume
        self.turnover = turnover
        self.transactions = transactions
        self.difference = difference

    @property
    def start_date(self):
        return self.start_datetime.date()

    @property
    def end_date(self):
        return self.end_datetime.date()

    @property
    def start_time(self):
        return self.start_datetime.time()

    @property
    def end_time(self):
        return self.end_datetime.time()
