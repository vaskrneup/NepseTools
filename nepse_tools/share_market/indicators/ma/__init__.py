import numpy as np
import pandas as pd

from nepse_tools.share_market.indicators.base_indicator import BaseIndicator


class MA(BaseIndicator):
    def __init__(
            self, ma_value: int,
            share_prices: list[list] | pd.DataFrame | dict[str, list],
            company_symbol: str = None,
            ma_from_column: str = BaseIndicator.DATA_COLUMNS.close,
            ma_value_key_name="ma",
            **kwargs
    ):
        super().__init__(share_prices, **kwargs)
        self.ma_value = ma_value
        self.company_symbol = company_symbol
        self.ma_from_column = ma_from_column
        self.ma_value_key_name = ma_value_key_name

        if company_symbol is not None:
            self.filters.append(lambda data: data[data[self.DATA_COLUMNS.symbol] == company_symbol])

    def process_data(self) -> list:
        column_data = self.DATA_COLUMNS.get_col_from_df(
            df=self.filter(self.share_prices),
            col=self.output_columns
        )

        if len(column_data[0]) < self.ma_value + 1:
            return []

        new_data = []
        start_point = 0
        end_point = 0

        while end_point < len(column_data[0]):
            end_point = start_point + self.ma_value

            new_data.append(
                {
                    **{
                        column: column_data[
                            self.output_column_index[column]
                        ][end_point - 1]
                        for column in self.output_columns
                    },
                    self.ma_value_key_name: np.sum(
                        column_data[
                            self.output_column_index[self.ma_from_column]
                        ][start_point:end_point]
                    ) / self.ma_value
                }
            )

            start_point += 1

        return new_data
