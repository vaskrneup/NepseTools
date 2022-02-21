import datetime
import pandas as pd

import requests
from bs4 import BeautifulSoup


class PriceScraper:
    DEFAULT_HTML_PARSER = "lxml"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        }
        self.token: str = ""

        self.establish_session()
        self.parse_share_price(datetime.date(year=2022, day=15, month=2))

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
        self.update_token(BeautifulSoup(main_page_resp.text, self.DEFAULT_HTML_PARSER))

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

    def parse_share_price(self, date: datetime.date, append_keys: bool = False):
        soup = BeautifulSoup(self.get_price_html(date), self.DEFAULT_HTML_PARSER)
        share_price_list = []

        if append_keys:
            keys = ["date", "time", *(self.normalize_text(key.text) for key in soup.select("thead tr th"))]
            share_price_list.append(keys)

        data_date = soup.select("h5 span.text-org")

        for tr in soup.select("tbody tr"):
            share_price_list.append([
                data_date and data_date[0].text.strip(),
                "00:00:00",
                *(
                    self.convert_datatype(
                        data.text.strip().replace(",", "")
                    ) for data in tr.select("td")
                )
            ])

        return share_price_list
