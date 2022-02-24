from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare
from nepse_tools.scraper.price_scraper import save_data_to_csv
from nepse_tools.share_market.indicators.ma import MA
from nepse_tools.share_market.notifiers.base_notifier import BaseNotifier


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


def notifier():
    BaseNotifier().send_email(
        subject="NEw MEssage  !!",
        receiver_emails=["bhaskar@vaskrneup.com"],
        attachment_file_path="test_img.jpg"
    )


notifier()
# price_scraper()
# ma_test()
