from nepse_tools.share_market.indicators.base_indicator import BaseIndicator
from nepse_tools.share_market.share_price.price_manager import PriceManager


class MA(BaseIndicator):
    def __init__(self, ma: int, share_price_manager: PriceManager):
        super().__init__(share_price_manager)
        self.ma = ma

    def process_data(self):
        new_data = []
        start_point = 0
        end_point = 0

        while end_point < len(self.share_price):
            end_point = start_point + self.ma
            new_data.append(
                {
                    "date": "",
                    "ma": sum([
                        share.closing_price for share in self.share_price[start_point:end_point]
                    ]) / self.ma
                }
            )
            start_point += 1

        self._processed_data = new_data
