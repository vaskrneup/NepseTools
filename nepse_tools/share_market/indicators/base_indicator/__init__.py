from typing import Any

from nepse_tools.share_market.share_price.price_manager import PriceManager


class BaseIndicator:
    def __init__(self, share_price_manager: PriceManager):
        self.share_price_manager = share_price_manager
        self.share_price = share_price_manager.share_price

        self._processed_data: Any = None

    def process_data(self) -> None:
        raise NotImplementedError()

    @property
    def processed_data(self) -> Any:
        if not self._processed_data:
            self.process_data()

        return self._processed_data
