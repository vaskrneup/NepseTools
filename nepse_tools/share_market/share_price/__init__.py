class SharePrice:
    def __init__(
            self, date: str, time: str,
            sno: int, symbol: str,
            conf: float,
            open_: float, high: float, low: float, close: float,
            vwap: float, vol: float, prev_close: float,
            turnover: float, trans: int, diff: float, range_: float,
            diff_percentage: float, range_percentage: float,
            vwap_percentage: float,
            days_120: float, days_180: float,
            weeks_high_52: float, weeks_low_52: float
    ):
        self.date = date
        self.time = time
        self.sno = sno
        self.symbol = symbol
        self.conf = conf
        self.open = open_
        self.high = high
        self.low = low
        self.close = close
        self.vwap = vwap
        self.vol = vol
        self.prev_close = prev_close
        self.turnover = turnover
        self.trans = trans
        self.diff = diff
        self.range = range_
        self.diff_percentage = diff_percentage
        self.range_percentage = range_percentage
        self.vwap_percentage = vwap_percentage
        self.days_120 = days_120
        self.days_180 = days_180
        self.weeks_low_52 = weeks_high_52
        self.weeks_high_52 = weeks_low_52
