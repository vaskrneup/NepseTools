from typing import Any

import numpy as np
import pandas as pd
from decouple import config


class DataColumns:
    date: str = "date"
    time: str = "time"
    sno: str = "sno"
    symbol: str = "symbol"
    conf: str = "conf"
    open: str = "open"
    high: str = "high"
    low: str = "low"
    close: str = "close"
    vwap: str = "vwap"
    vol: str = "vol"
    prev_close: str = "prev_close"
    turnover: str = "turnover"
    trans: str = "trans"
    diff: str = "diff"
    range: str = "range"
    diff_percentage: str = "diff_percentage"
    range_percentage: str = "range_percentage"
    vwap_percentage: str = "vwap_percentage"
    days_120: str = "120_days"
    days_180: str = "180_days"
    weeks_high_52: str = "52_weeks_high"
    weeks_low_52: str = "52_weeks_low"

    AVAILABLE_COLUMNS = {
        date, time, sno, symbol, conf, open, high, low, close, vwap, vol, prev_close, turnover, trans,
        diff, range, diff_percentage, range_percentage, vwap_percentage, days_120, days_180,
        weeks_high_52, weeks_low_52
    }

    def get_col_from_df(
            self, df: pd.DataFrame, col: list[str] | str,
            data_type: list | np.ndarray = np.ndarray
    ) -> list | np.ndarray:
        if type(col) is str and col not in self.AVAILABLE_COLUMNS:
            raise ValueError(f"`{col=}` is not a valid column.")
        elif type(col) is list and len(set(col).difference(self.AVAILABLE_COLUMNS)) != 0:
            raise ValueError(f"`{','.join(set(col).difference(self.AVAILABLE_COLUMNS))}` are not a valid column.")

        if data_type is list:
            return df[col].to_list() if type(col) is str else [df[_col].to_list() for _col in col]
        elif data_type is np.ndarray:
            return df[col].to_numpy() if type(col) is str else [df[_col].to_numpy() for _col in col]
        else:
            raise ValueError(f"`{data_type=}` not of type, `list` or `np.ndarray`")


class BaseIndicator:
    DATA_COLUMNS = DataColumns()

    def __init__(
            self,
            share_prices: list[list] | pd.DataFrame | dict[str, list],
            output_columns: list[str],
            filters: list[callable] = None,
            company_symbol: str = None,
            **kwargs
    ):
        if isinstance(share_prices, pd.DataFrame):
            self.share_prices: pd.DataFrame = share_prices
        else:
            self.share_prices: pd.DataFrame = pd.DataFrame(share_prices)

        self.kwargs = kwargs
        self.output_columns = output_columns
        self.filters = filters or []
        self.company_symbol = company_symbol
        self._processed_data: Any = None

        self.output_column_index = {
            column: i
            for i, column in enumerate(output_columns)
        }

    @property
    def processed_data(self):
        if self._processed_data is None:
            self._process_data()

        return self._processed_data

    def process_data(self):
        raise NotImplementedError()

    def _process_data(self):
        self._processed_data = self.process_data()

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        final_data = data

        for _filter in self.filters:
            final_data = _filter(final_data)

        return final_data

    @classmethod
    def create_indicator_from_csv_file(
            cls, *, csv_file_path: str = config("SHARE_PRICE_STORAGE_LOCATION"), **kwargs
    ):
        kwargs.setdefault(
            "share_prices",
            pd.read_csv(csv_file_path)
        )
        return cls(**kwargs)
