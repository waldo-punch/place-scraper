import logging
import time
import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from media.base import ScrapBase
from utils.date_parser import get_now

GOOGLE_MAP_PAGE = 'https://www.google.co.kr/maps/'


class GooglePlace(ScrapBase):

    def __init__(self, store_id: str, store_name: str, status: str, debug=False):
        self.debug = debug
        # google store id는 data=? 형태의 url path
        self.store_id = store_id
        self.store_name = store_name

        # N : 신규, P : 수집중, E : 수집 종료
        self.status = status
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()

        self.__access_place()
        self.store_info = {}
        self.review_list = []

    def run(self):
        self.__access_place()
        self.store_info = self.get_place_basic_info()
        self.review_list.append(self.get_reviews())

    def __get_driver(self, debug=False):
        options = Options()

        if not self.debug:
            options.add_argument("--headless")
        else:
            options.add_argument("--window-size=1366,768")
        input_driver = webdriver.Chrome(options=options)

        return input_driver

    def __get_logger(self):
        logger = logging.getLogger('googlemaps-scraper')
        logger.setLevel(logging.DEBUG)
        return logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb)

        self.driver.close()
        self.driver.quit()

        return True

    def __access_place(self):
        try:
            self.driver.get(GOOGLE_MAP_PAGE)
        except Exception as e:
            self.driver.quit()
            self.driver = self.__get_driver()
            self.driver.get(GOOGLE_MAP_PAGE)
        time.sleep(2)
        # google 검색란에 매장명 입력
        text_input = self.driver.find_element(By.ID, "searchboxinput")
        ActionChains(self.driver).send_keys_to_element(text_input, self.store_id).perform()
        time.sleep(0.5)
        # 검색
        text_input.send_keys(Keys.RETURN)
        time.sleep(2.4)

    def get_reviews(self):
        review_button = self.driver.find_element(By.CSS_SELECTOR, '#QA0Szd > div > div > div.w6VYqd > div.bJzME.tTVLSc > div > div.e07Vkf.kA9KIf > div > div > div:nth-child(3) > div > div > button:nth-child(2)')
        print(review_button)
        ActionChains(self.driver).click(review_button)
        time.sleep(2)
        response = BeautifulSoup(self.driver.page_source, 'html.parser')
        blocks = response.find_all('div', class_='jftiEf fontBodyMedium ')

        review_list = []
        for review in blocks:
            review_list.append(self.__parse_review(review))
        return review_list

    def __parse_review(self, review):

        item = {}

        try:
            id_review = review['data-review-id']
        except Exception as e:
            id_review = None

        try:
            username = review['aria-label']
        except Exception as e:
            username = None

        try:
            review_text = self.__filter_string(review.find('span', class_='wiI7pd').text)
        except Exception as e:
            review_text = None

        try:
            rating = float(review.find('span', class_='kvMYJc')['aria-label'].split(' ')[0])
        except Exception as e:
            rating = None

        try:
            relative_date = review.find('span', class_='rsqaWe').text
        except Exception as e:
            relative_date = None

        try:
            user_url = review.find('button', class_='WEBjve')['data-href']
        except Exception as e:
            user_url = None

        item['comment_id'] = id_review
        item['comment'] = review_text
        item['date'] = relative_date

        # store datetime of scraping and apply further processing to calculate
        # correct date as retrieval_date - time(relative_date)
        item['retrieval_date'] = get_now()
        item['rating'] = rating
        item['username'] = username
        # item['n_photo_user'] = n_photos  ## not available anymore
        item['user_link'] = user_url

        return item

    def get_comments(self):
        pass

    def get_place_basic_info(self):
        html = self.driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        info_set = soup.select('.CsEnBe')
        place_info = self.parse_html(info_set)
        name = soup.find('h1','DUwDvf').get_text()
        place_info['name'] = name

        return place_info

    def parse_html(self, selected):
        for each in selected:
            label_ = each['aria-label']

            if label_.startswith("주소: "):
                address = label_.split("주소: ")[1]

            if label_.startswith("전화: "):
                phone = label_.split("전화: ")[1]

            if label_.startswith("웹사이트: "):
                link = each['href']

            if label_.startswith("웹사이트: "):
                link = label_.split("웹사이트: ")[1]

            if label_.startswith("메뉴"):
                menu = each['href']

            if label_.startswith("예약하기"):
                book = each['href']

        place_info = {
            'address': address,
            'phone': phone,
            'link': link,
            'menu': menu,
            'book': book,
        }
        return place_info