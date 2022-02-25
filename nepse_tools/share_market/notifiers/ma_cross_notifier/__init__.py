import datetime

import pandas as pd

from nepse_tools.scraper.price_scraper import PriceScraper
from nepse_tools.share_market.indicators.moving_average import MA
from nepse_tools.share_market.notifiers.base_notifier import BaseNotifier


class MACrossNotifier(BaseNotifier):
    def __init__(self, ma_big: int, ma_small: int, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ma_big = ma_big
        self.ma_small = ma_small

    def process_data(self, email: str = None, *args, **kwargs) -> dict | None:
        today_share_price = PriceScraper().parse_share_price(
            date=datetime.datetime.now().date()
        )

        if today_share_price is None:
            return None
        else:
            today_share_price = pd.DataFrame(today_share_price)

        mas = [
            [
                MA(
                    ma_value=self.ma_big,
                    share_prices=self.share_price_df,
                    company_symbol=symbol,
                ),
                MA(
                    ma_value=self.ma_small,
                    share_prices=self.share_price_df,
                    company_symbol=symbol,
                )
            ] for symbol in self.scripts
        ]
        old_mas_processed_data = [
            [
                ma_big.process_data()[-(self.ma_big - 1):],
                ma_small.process_data()[-(self.ma_small - 1):]
            ]
            for ma_big, ma_small in mas
        ]

        prev_ma = [
            [
                ma_big[-1]["moving_average"],
                ma_small[-1]["moving_average"]
            ] for ma_big, ma_small in old_mas_processed_data
        ]

        current_ma = [
            [
                PriceScraper.convert_to_float(
                    (
                            sum((data[MA.DATA_COLUMNS.close] for data in ma_big))
                            + today_share_price[
                                today_share_price[MA.DATA_COLUMNS.symbol] == ma_big[0][MA.DATA_COLUMNS.symbol]
                                ][
                                MA.DATA_COLUMNS.close
                            ].values[0]
                    ) / self.ma_big
                ),
                PriceScraper.convert_to_float(
                    (
                            sum((data[MA.DATA_COLUMNS.close] for data in ma_small))
                            + today_share_price[
                                today_share_price[MA.DATA_COLUMNS.symbol] == ma_big[0][MA.DATA_COLUMNS.symbol]
                                ][
                                MA.DATA_COLUMNS.close
                            ].values[0]
                    ) / self.ma_small
                ),
            ] for ma_big, ma_small in old_mas_processed_data
        ]

        print(prev_ma)
        print(current_ma)

        # return self.email_manager.get_send_mail_kwargs(
        #     subject=""
        # )
