import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup


class PriceScraper:
    DEFAULT_HTML_PARSER = "lxml"

    def __init__(self):
        self.session = None
        self.token: str = ""

        self.share_price_keys = []
        self.share_price_keys_set = set()

        self.reset_session()

    def reset_session(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        }
        self.establish_session()

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
                out = float(text)
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
        date_text = soup.select("h5 span.text-org")

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
                date_text and date_text[0].text.strip(),
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
