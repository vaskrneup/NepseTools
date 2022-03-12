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

    def process_data(self, email: str = None, today_share_price: dict = None, *args, **kwargs) -> dict | None:
        if today_share_price is None:
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
                    filters=[lambda data: data.tail(self.ma_big * 2)]
                ),
                MA(
                    ma_value=self.ma_small,
                    share_prices=self.share_price_df,
                    company_symbol=symbol,
                    filters=[lambda data: data.tail(self.ma_small * 2)]
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

        current_ma = []
        prev_ma = []

        for ma_big, ma_small in old_mas_processed_data:
            if not ma_big or not ma_small:
                current_ma.append([None, None])
                prev_ma.append([None, None])
                continue

            if ma_big[0][MA.DATA_COLUMNS.symbol] != ma_small[0][MA.DATA_COLUMNS.symbol]:
                raise ValueError(f"Column Mismatch \n\n{ma_big=}\n\n{ma_small=}")

            today_closing_price = today_share_price[
                today_share_price[MA.DATA_COLUMNS.symbol] == ma_big[0][MA.DATA_COLUMNS.symbol]
                ][
                MA.DATA_COLUMNS.close
            ].values

            if not today_closing_price:
                current_ma.append([None, None])
                prev_ma.append([None, None])
                continue

            new_ma_big = sum([
                *(_ma_big[MA.DATA_COLUMNS.close] for _ma_big in ma_big),
                today_closing_price[0]
            ]) / self.ma_big

            new_ma_small = sum([
                *(_ma_small[MA.DATA_COLUMNS.close] for _ma_small in ma_small),
                today_closing_price[0]
            ]) / self.ma_small

            current_ma.append([
                PriceScraper.convert_to_float(new_ma_big),
                PriceScraper.convert_to_float(new_ma_small)
            ])
            prev_ma.append([
                PriceScraper.convert_to_float(ma_big[-1]["moving_average"]),
                PriceScraper.convert_to_float(ma_small[-1]["moving_average"])
            ])

        i = -1

        for prev_ma_data, current_ma_data in zip(prev_ma, current_ma):
            i += 1

            if None in {*prev_ma_data, *current_ma_data}:
                continue

            if prev_ma_data[0] < prev_ma_data[1] and current_ma_data[0] > current_ma_data[1]:
                print(self.scripts[i], "DECREASING")
            elif prev_ma_data[0] > prev_ma_data[1] and current_ma_data[0] < current_ma_data[1]:
                print(self.scripts[i], "INCREASING")
            else:
                pass

        # return self.email_manager.get_send_mail_kwargs(
        #     subject=""
        # )
