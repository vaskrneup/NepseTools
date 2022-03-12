import datetime

import numpy as np
from matplotlib import pyplot as plt

from nepse_tools.share_market.indicators.base_indicator import BaseIndicator


class MA(BaseIndicator):
    def __init__(
            self,
            ma_value: int,
            ma_from_column: str = BaseIndicator.DATA_COLUMNS.close,
            ma_value_key_name="moving_average",
            **kwargs
    ):
        kwargs.setdefault(
            "output_columns",
            [
                self.DATA_COLUMNS.symbol,
                self.DATA_COLUMNS.date,
                self.DATA_COLUMNS.close,
                self.DATA_COLUMNS.vol
            ]
        )
        super().__init__(**kwargs)
        self.ma_value = ma_value
        self.ma_from_column = ma_from_column
        self.ma_value_key_name = ma_value_key_name

        if self.company_symbol is not None:
            self.filters = [lambda data: data[data[self.DATA_COLUMNS.symbol] == self.company_symbol], *self.filters]

    def process_data(self) -> list:
        column_data = self.DATA_COLUMNS.get_col_from_df(
            df=self.filter(self.share_prices),
            col=self.output_columns
        )

        start_point = 0
        end_point = 0

        if len(column_data[0]) < self.ma_value + 1:
            return []

        new_data = []

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

    @staticmethod
    def plot_graph(mas_from: list[list[int]], company_symbol: str):
        ma_classes = [
            MA.create_indicator_from_csv_file(
                ma_value=ma[0], company_symbol=company_symbol,
                output_columns=[
                    MA.DATA_COLUMNS.symbol,
                    MA.DATA_COLUMNS.date,
                    MA.DATA_COLUMNS.close,
                    MA.DATA_COLUMNS.vol
                ]
            ) for ma in mas_from
        ]
        first = True

        fig, ax = plt.subplots(2, gridspec_kw={'height_ratios': [2, 1]}, sharex='col')

        for mas, class_ in zip(mas_from, ma_classes):
            if first is True:
                ax[0].plot(
                    [
                        datetime.datetime.strptime(data[MA.DATA_COLUMNS.date], "%Y-%m-%d").date()
                        for data in class_.processed_data
                    ],
                    [
                        data[class_.ma_from_column] for data in class_.processed_data
                    ],
                    label=class_.ma_from_column.replace("_", " ").capitalize()
                )
                ax[1].plot(
                    [
                        datetime.datetime.strptime(data[MA.DATA_COLUMNS.date], "%Y-%m-%d").date()
                        for data in class_.processed_data
                    ],
                    [
                        data[MA.DATA_COLUMNS.vol] for data in class_.processed_data
                    ],
                    label="Volume"
                )

            ax[0].plot(
                [
                    datetime.datetime.strptime(data[MA.DATA_COLUMNS.date], "%Y-%m-%d").date()
                    for data in class_.processed_data
                ],
                [
                    data["moving_average"] for data in class_.processed_data
                ],
                label=f"MA-{mas[0]}"
            )
            first = False

        ax[0].xaxis.set_tick_params(rotation=30, labelsize=10)
        ax[0].legend(loc='lower right')
        ax[1].legend(loc='lower right')
        fig.suptitle(f"Plot of {company_symbol}")
        ax[0].grid()
        ax[1].grid()
        return fig, ax, plt


MovingAverage = MA
