from nepse_tools.share_market.share_price import SharePrice


class PriceManager:
    def __init__(self, share_price: list[SharePrice]):
        self.share_price = share_price
