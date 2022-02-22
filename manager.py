from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare
from nepse_tools.scraper.price_scraper import save_data_to_csv, date_range
from nepse_tools.share_market.indicators.ma import MA
from nepse_tools.share_market.share_price.price_manager import PriceManager


def meroshare():
    ms = MeroShare(
        dp=config("MEROSHARE_DP"),
        username=config("MEROSHARE_USERNAME"),
        password=config("MEROSHARE_PASSWORD")
    )
    ms.login()


# def ma_test():
#     x = MA(ma=5, share_price_manager=PriceManager(share_price=SHARE_DATA))
#     print(x.processed_data)


def price_scraper():
    save_data_to_csv()
    # save_data_to_csv()
    # x = PriceScraper().parse_share_price(datetime.date(year=2022, day=15, month=2), append_keys=True)


price_scraper()
