import datetime
import os.path
from typing import Iterable

import pandas as pd
from decouple import config

from nepse_tools.scraper.price_scraper.scraper import PriceScraper
from nepse_tools.share_market.indicators.base_indicator import DataColumns
from nepse_tools.utils.logger import logger


def date_range(start: str | datetime.date, end: str | datetime.date = datetime.datetime.now().date()):
    start_datetime = start
    end_datetime = end
    time_delta = datetime.timedelta(days=1)

    if type(start) is str:
        start_datetime = datetime.datetime.strptime(start, "%Y-%m-%d").date()
    if type(end) is str:
        end_datetime = datetime.datetime.strptime(end, "%Y-%m-%d").date()

    while start_datetime < end_datetime:
        start_datetime += time_delta
        yield start_datetime


def save_data_to_csv(date_generator: Iterable | None = None, csv_path: str = config("SHARE_PRICE_STORAGE_LOCATION")):
    price_scraper = PriceScraper()
    scraped_data = {
        key: [] for key in price_scraper.share_price_keys
    }
    scraped_data_df = pd.DataFrame()

    if os.path.exists(csv_path):
        scraped_data_df = pd.read_csv(
            csv_path,
            converters=DataColumns.COLUMN_DATA_TYPE_CONVERTER
        )

    if date_generator is None:
        if scraped_data_df.empty:
            last_date = pd.read_csv(
                csv_path,
                converters=DataColumns.COLUMN_DATA_TYPE_CONVERTER
            ).tail(1)["date"].values[0]
        else:
            last_date = scraped_data_df.tail(1)["date"].values[0]

        date_generator = date_range(last_date, datetime.datetime.now().date())

    for date in date_generator:
        logger.info(f"Scraping `{date}`")

        if price_data := price_scraper.parse_share_price(date=date):
            for key in scraped_data:
                scraped_data[key] = [*scraped_data[key], *price_data[key]]
            logger.success(f"Scraped `{date}`")
        else:
            logger.error(f"No Data Available For `{date}`")

    scraped_data_df = pd.concat(
        [scraped_data_df, pd.DataFrame(scraped_data)]
    ).reset_index().drop_duplicates()

    for col in DataColumns.COLUMN_DATA_TYPE_CONVERTER:
        logger.info(f"Datatype verification on `{col}`")
        scraped_data_df[col].apply(DataColumns.COLUMN_DATA_TYPE_CONVERTER[col])
        logger.success(f"Data verified for `{col}`")

    logger.info(f"Saving data to csv at: `{csv_path}`")
    scraped_data_df.to_csv(csv_path, columns=price_scraper.share_price_keys)
    logger.success(f"Data saved to csv at: `{csv_path}`")
