from decouple import config

from nepse_tools.platforms.meroshare.api import MeroShare
from nepse_tools.scraper.price_scraper import save_data_to_csv
from nepse_tools.share_market.indicators.moving_average import MA
from nepse_tools.share_market.notifiers import BulkNotifier, MACrossNotifier


def meroshare():
    ms = MeroShare(
        dp=config("MEROSHARE_DP"),
        username=config("MEROSHARE_USERNAME"),
        password=config("MEROSHARE_PASSWORD"),
        pin=config("MEROSHARE_PIN"),
    )
    ms.login()
    # print(ms.apply_for_ipo(
    #     auto_apply_all=True
    # ))
    print(ms.bank_id_from_bank_list_view)
    print(ms.bank_code_from_bank_list_view)
    print(ms.bank_account_branch_from_bank_detail_view)
    print(ms.bank_account_number_from_bank_detail_view)
    print(ms.bank_id_from_bank_detail_view)
    print(ms.bank_branch_id_from_bank_detail_view)
    print(ms.id_from_bank_detail_view)


def ma_test():
    fig, _, plt = MA.plot_graph(mas_from=[[5], [20]], company_symbol="GBIME")
    plt.show()
    fig.savefig("text.jpg")


def price_scraper():
    save_data_to_csv()
    # save_data_to_csv()
    # x = PriceScraper().parse_share_price(datetime.date(year=2022, day=15, month=2), append_keys=True)


def notifier():
    bulk_notifier = BulkNotifier(
        notifiers=[
            MACrossNotifier(
                notification_emails=["vaskrneup@gmail.com", "bhaskar.neupane.58@gmail.com"],
                company_symbol=["GBIME", "NRIC", "NMB"],
                ma_big=20,
                ma_small=5
            )
        ]
    )
    print(bulk_notifier.run())


meroshare()
# notifier()
# price_scraper()
# ma_test()
