import datetime
import random

from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare
from nepse_tools.scraper.price_scraper import PriceScraper
from nepse_tools.share_market.indicators.ma import MA
from nepse_tools.share_market.share_price import SharePrice
from nepse_tools.share_market.share_price.price_manager import PriceManager

SHARE_DATA = [
    SharePrice(
        start_datetime=datetime.datetime.now(),
        end_datetime=datetime.datetime.now(),
        low_price=random.randint(300, 900),
        high_price=random.randint(300, 900),
        closing_price=random.randint(300, 900),
        opening_price=random.randint(300, 900),
        volume=random.randint(300, 900),
        turnover=random.randint(300, 900),
        difference=random.randint(300, 900),
        transactions=random.randint(300, 900)
    ) for _ in range(300)
]


def meroshare():
    ms = MeroShare(
        dp=config("MEROSHARE_DP"),
        username=config("MEROSHARE_USERNAME"),
        password=config("MEROSHARE_PASSWORD")
    )
    ms.login()


def ma_test():
    x = MA(ma=5, share_price_manager=PriceManager(share_price=SHARE_DATA))
    print(x.processed_data)


def price_scraper():
    PriceScraper()


price_scraper()
