import pandas as pd
from decouple import config

from nepse_tools.share_market.share_price import SharePrice


class PriceManager:
    CSV_TO_OBJECT_MAP = {
        "120_days": "days_120",
        "180_days": "days_180",
        "52_weeks_low": "weeks_low_52",
        "52_weeks_high": "weeks_high_52",
    }

    def __init__(self, share_price: list[SharePrice] = None):
        self.share_price = share_price


class DataManager:
    def __init__(self, csv_path: str = config("SHARE_PRICE_STORAGE_LOCATION")):
        self.csv_path = csv_path
        self.share_price_df = pd.read_csv(csv_path)
