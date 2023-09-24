# Import necessary libraries and modules
from typing import Any
import numpy as np
import pandas as pd
from decouple import config
from nepse_tools.scraper.price_scraper.scraper import PriceScraper

class DataColumns:
    """
    A class to manage constants related to data columns.
    
    This class defines constants for column names, data types, and conversion functions.
    """

    # Define constants for column names
    date: str = "date"
    time: str = "time"
    sno: str = "sno"
    symbol: str = "symbol"
    # ... (other column names)

    # Define a set of available columns
    AVAILABLE_COLUMNS = {date, time, sno, symbol, ...}

    # Define data types for each column
    COLUMN_DATA_TYPE = {date: str, time: str, sno: int, symbol: str, ...}

    # Define data type converter functions for each column
    COLUMN_DATA_TYPE_CONVERTER = {date: PriceScraper.convert_to_str, time: PriceScraper.convert_to_int, ...}

    def get_col_from_df(self, df: pd.DataFrame, col: list[str] | str, data_type: list | np.ndarray = np.ndarray) -> list | np.ndarray:
        """
        Extract specified columns from a DataFrame with optional data type conversion.

        Args:
            df (pd.DataFrame): The DataFrame from which columns will be extracted.
            col (list[str] | str): The column(s) to extract.
            data_type (list | np.ndarray, optional): Desired data type for the extracted column(s).
                Defaults to np.ndarray.

        Returns:
            list | np.ndarray: Extracted column(s) with optional data type conversion.
        Raises:
            ValueError: If an invalid column name is provided.
        """
        # Check if the specified column(s) are valid
        if type(col) is str and col not in self.AVAILABLE_COLUMNS:
            raise ValueError(f"`{col=}` is not a valid column.")
        elif type(col) is list and len(set(col).difference(self.AVAILABLE_COLUMNS)) != 0:
            raise ValueError(f"`{','.join(set(col).difference(self.AVAILABLE_COLUMNS))}` are not valid columns.")

        # Extract the specified column(s) and apply data type conversion
        if data_type is list:
            return df[col].to_list() if type(col) is str else [df[_col].to_list() for _col in col]
        elif data_type is np.ndarray:
            return df[col].to_numpy() if type(col) is str else [df[_col].to_numpy() for _col in col]
        else:
            raise ValueError(f"`{data_type=}` is not of type `list` or `np.ndarray`")

class BaseIndicator:
    """
    A base class for creating indicators from share price data.

    This class provides a foundation for creating custom indicators based on share price data.
    """

    DATA_COLUMNS = DataColumns()

    def __init__(
            self,
            share_prices: list[list] | pd.DataFrame | dict[str, list],
            output_columns: list[str],
            filters: list[callable] = None,
            company_symbol: str = None,
            **kwargs
    ):
        """
        Initialize the BaseIndicator.

        Args:
            share_prices (list[list] | pd.DataFrame | dict[str, list]): Share price data.
            output_columns (list[str]): List of output column names.
            filters (list[callable], optional): List of filter functions to apply to the data. Defaults to None.
            company_symbol (str, optional): Symbol of the company for which the indicator is created. Defaults to None.
            **kwargs: Additional keyword arguments.
        """
        # Convert input data into a DataFrame if it's not already
        if isinstance(share_prices, pd.DataFrame):
            self.share_prices: pd.DataFrame = share_prices
        else:
            self.share_prices: pd.DataFrame = pd.DataFrame(share_prices)

        self.kwargs = kwargs
        self.output_columns = output_columns
        self.filters = filters or []
        self.company_symbol = company_symbol
        self._processed_data: Any = None

        # Create a dictionary to map output column names to their indices
        self.output_column_index = {
            column: i
            for i, column in enumerate(output_columns)
        }

    @property
    def processed_data(self):
        """
        Property to access processed data.

        Returns:
            Any: Processed data.
        """
        if self._processed_data is None:
            self._process_data()

        return self._processed_data

    def process_data(self):
        """
        Abstract method to be implemented by derived classes for data processing.

        Raises:
            NotImplementedError: This method should be overridden in derived classes.
        """
        raise NotImplementedError()

    def _process_data(self):
        """
        Internal method to process data and set the processed_data property.
        """
        self._processed_data = self.process_data()

    def filter(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Apply filter functions to the data.

        Args:
            data (pd.DataFrame): Input data.

        Returns:
            pd.DataFrame: Filtered data.
        """
        final_data = data

        for _filter in self.filters:
            final_data = _filter(final_data)

        return final_data

    @classmethod
    def create_indicator_from_csv_file(
            cls,
            *,
            csv_file_path: str | pd.DataFrame = config("SHARE_PRICE_STORAGE_LOCATION"),
            **kwargs
    ):
        """
        Create an indicator instance from a CSV file.

        Args:
            csv_file_path (str | pd.DataFrame, optional): Path to the CSV file or a DataFrame containing share price data.
                Defaults to the value from the config file.
            **kwargs: Additional keyword arguments.

        Returns:
            BaseIndicator: An instance of the derived class.
        """
        if type(csv_file_path) is str:
            data = pd.read_csv(csv_file_path)
        else:
            data = csv_file_path

        kwargs.setdefault(
            "share_prices",
            data
        )
        return cls(**kwargs)
