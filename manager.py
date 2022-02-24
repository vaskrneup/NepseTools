from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare
from nepse_tools.scraper.price_scraper import save_data_to_csv
from nepse_tools.share_market.indicators.ma import MA


def meroshare():
    ms = MeroShare(
        dp=config("MEROSHARE_DP"),
        username=config("MEROSHARE_USERNAME"),
        password=config("MEROSHARE_PASSWORD")
    )
    ms.login()
    print(ms.crn_number)


def ma_test():
    MA.plot_graph(mas_from=[[5], [20]], company_symbol="GBIME")


def price_scraper():
    save_data_to_csv()
    # save_data_to_csv()
    # x = PriceScraper().parse_share_price(datetime.date(year=2022, day=15, month=2), append_keys=True)


# price_scraper()
ma_test()
