"""
Price scraper using sharesansar, you can create

Contribution:
    You can upgrade the scrapers, make them more efficient or add new functionality.

Notes:
    * Please create and run tests, if you update anything.
"""

import datetime
from typing import Any

import pandas as pd
import requests
from bs4 import BeautifulSoup
from decouple import config

from nepse_tools.utils.logger import logger


class PriceScraper:
    """
    Share Price scraper using `sharesansar`.
    Additionally, it provides number of different companies.
    """
    DEFAULT_HTML_PARSER = "lxml"

    def __init__(self):
        self.session = None
        self.token: str = ""

        self.share_price_keys = []
        self.share_price_keys_set = set()

        self.share_price_df: None | pd.DataFrame = None

        self.reset_session()

    def load_share_price_df_if_required(self):
        if self.share_price_df is None:
            self.share_price_df = pd.read_csv(config("SHARE_PRICE_STORAGE_LOCATION"))

    def reset_session(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        }
        self.establish_session()

    @staticmethod
    def convert_to_float(text: str):
        try:
            return round(float(text), 2)
        except (ValueError, TypeError):
            return 0.0

    @staticmethod
    def convert_to_int(text: str):
        try:
            return int(text)
        except (ValueError, TypeError):
            return 0

    @staticmethod
    def convert_to_str(text: Any):
        try:
            return str(text)
        except Exception as e:
            logger.error(str(e))
            return ""

    @staticmethod
    def normalize_text(text: str):
        text = text.lower().strip()
        normalized_text = ""

        for letter in text:
            if letter == " ":
                normalized_text += "_"
            elif letter == "%":
                normalized_text += "percentage"
            elif letter.isalnum():
                normalized_text += letter

        return normalized_text.strip("_")

    @staticmethod
    def convert_datatype(text: str):
        text = str(text)

        try:
            if "." in text:
                out = round(float(text), 2)
            else:
                out = int(text)
        except ValueError:
            out = text

        return out

    @staticmethod
    def get_formatted_date_from_date(date: datetime.date):
        return f"{date.year}" \
               f"-{date.month if date.month > 9 else f'0{date.month}'}-" \
               f"{date.day if date.day > 9 else f'0{date.day}'}"

    def update_token(self, soup):
        if token := soup.select("meta[name=_token]"):
            self.token = token[0].attrs.get("content")

    def establish_session(self):
        main_page_resp = self.session.get("https://www.sharesansar.com/today-share-price")
        main_page_soup = BeautifulSoup(main_page_resp.text, self.DEFAULT_HTML_PARSER)

        self.share_price_keys = [
            "date", "time",
            *(
                self.normalize_text(key.text)
                for key in main_page_soup.select("thead tr th")
            )
        ]
        self.share_price_keys_set = set(self.share_price_keys)
        self.update_token(main_page_soup)

    def get_price_html(self, date: datetime.date):
        if datetime.datetime.now().date() == date:
            resp = self.session.get(
                "https://www.sharesansar.com/today-share-price",
                headers=self.session.headers
            )
        else:
            resp = self.session.post(
                "https://www.sharesansar.com/ajaxtodayshareprice",
                data={
                    "_token": self.token,
                    "sector": "all_sec",
                    "date": self.get_formatted_date_from_date(date)
                },
                headers={
                    **self.session.headers,
                    "x-requested-with": "XMLHttpRequest"
                }
            )
        return resp.text

    def parse_share_price(self, date: datetime.date) -> dict | None:
        soup = BeautifulSoup(self.get_price_html(date), self.DEFAULT_HTML_PARSER)

        if datetime.datetime.now().date() == date:
            date_text = self.get_formatted_date_from_date(date)
        else:
            date_text = soup.select("h5 span.text-org")
            date_text = date_text and date_text[0].text.strip()

        current_keys = [
            "date", "time",
            *(
                self.normalize_text(key.text)
                for key in soup.select("thead tr th")
            )
        ]
        current_keys_set = set(current_keys)
        parsed_data = {
            key: [] for key in self.share_price_keys
        }

        for tr in soup.select("tbody tr"):
            parsed_price_data = [
                date_text,
                "00:00:00",
                *(
                    self.convert_datatype(data.text.strip().replace(",", ""))
                    for data in tr.select("td")
                    if data
                )
            ]

            if len(parsed_price_data) < len(current_keys):
                return None
            else:
                for key, value in zip(current_keys, parsed_price_data):
                    parsed_data[key].append(value)

                for key in self.share_price_keys_set.difference(current_keys_set):
                    parsed_data[key].append(None)

        return parsed_data

    def get_all_company_symbol(self, n: int = 1000):
        from nepse_tools.share_market.indicators.base_indicator import DataColumns

        self.load_share_price_df_if_required()
        return list(set(self.share_price_df[DataColumns.symbol].tail(n).to_list()))
