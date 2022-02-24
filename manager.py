import datetime

from decouple import config
import matplotlib.pyplot as plt

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
    mas_from = [[50], [200]]
    ma_classes = [
        MA.create_indicator_from_csv_file(
            ma_value=ma[0], company_symbol="GBIME",
            output_columns=[
                MA.DATA_COLUMNS.symbol,
                MA.DATA_COLUMNS.date,
                MA.DATA_COLUMNS.close
            ]
        ) for ma in mas_from
    ]
    first = True

    fig, ax = plt.subplots()

    for mas, class_ in zip(mas_from, ma_classes):
        if first is True:
            plt.plot(
                [
                    datetime.datetime.strptime(data[MA.DATA_COLUMNS.date], "%Y-%m-%d").date()
                    for data in class_.processed_data
                ],
                [
                    data[MA.DATA_COLUMNS.close] for data in class_.processed_data
                ],
                label=f"Closing Price"
            )

        plt.plot(
            [
                datetime.datetime.strptime(data[MA.DATA_COLUMNS.date], "%Y-%m-%d").date()
                for data in class_.processed_data
            ],
            [
                data["ma"] for data in class_.processed_data
            ],
            label=f"MA {mas[0]}"
        )
        first = False

    ax.xaxis.set_tick_params(rotation=30, labelsize=10)
    plt.legend(loc='upper center')
    plt.show()


def price_scraper():
    save_data_to_csv()
    # save_data_to_csv()
    # x = PriceScraper().parse_share_price(datetime.date(year=2022, day=15, month=2), append_keys=True)


# price_scraper()
ma_test()
