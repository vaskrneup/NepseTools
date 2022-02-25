from nepse_tools.share_market.notifiers.base_notifier import BaseNotifier


class MACrossNotifier(BaseNotifier):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def process_data(self, email: str = None, *args, **kwargs) -> dict | None:
        pass
