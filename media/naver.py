from media.base import ScrapBase
from utils.http_request import Get
from selenium import  webdriver
from bs4 import BeautifulSoup


class NaverPlace(ScrapBase):
    headers = {
        'User-Agent': 'Mozilla',
        'content-type': 'application/json',
    }

    def __init__(self, store_id: str, store_name: str) -> None:
        self.store_id = store_id
        self.store_name = store_name
        self.store_info = {}

    def attach_headers(self, headers: dict) -> None:
        self.headers = headers

    def get_reviews(self):
        driver = webdriver.Chrome()

        pass

    def get_comments(self):
        pass

    def get_place_basic_info(self):
        url = f'https://map.naver.com/v5/api/sites/summary/{self.store_id}?lang=ko'
        try:
            get = Get(url, self.headers)
            data = get.request()
            store_info = {
                'place_id': data['id'],
                'description': data['description'],
                'name': data['name'],
                'geoX': data['x'],
                'geoY': data['y'],
                'address': data['address'],
                'roadAddress': data['roadAddr']['text'],
                'phone': data['phone'],
                'keywords': data['keywords'],
            }

            return store_info
        except KeyError:
            # Todo 에러처리
            return
        pass

    def parse_html(self, text):
        pass
