import logging
import time
import traceback

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

from media.base import ScrapBase
from utils.date_parser import *
from utils.http_request import Get

class NaverPlace(ScrapBase):
    def get_comments(self):
        pass

    def parse_html(self, text):
        pass

    headers = {
        'User-Agent': 'Mozilla',
        'content-type': 'application/json',
    }

    def __init__(self, store_id: str, store_name: str, status: str) -> None:
        self.store_id = store_id
        self.store_name = store_name

        # N : 신규, P : 수집중, E : 수집 종료
        self.status = status
        self.driver = self.__get_driver()
        self.logger = self.__get_logger()

        self.store_info = {}
        self.review_list = []

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_val, exc_tb)

        self.driver.close()
        self.driver.quit()

        return True
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

    def attach_headers(self, headers: dict) -> None:
        self.headers = headers

    def get_reviews(self):
        try:
            url = f'https://m.place.naver.com/restaurant/{self.store_id}/review/visitor?reviewSort=recent'
            self.driver.get(url)
            time.sleep(2)
            # Pagedown
            self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.END)

            cnt = 0
            # 신규, 크롤링에 따른 더보기 값 처리
            while True:
                try:
                    self.driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div/div/div[7]/div[2]/div[3]/div[2]').click()
                    self.driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
                    time.sleep(0.5)

                    # ToDo 로직 추가구현 필요
                    if self.status == 'P' and cnt >= 3:
                        break
                    cnt += 1
                except Exception as err:
                    print(err)
                    break

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            review_lists = soup.select(
                '#app-root > div > div > div > div:nth-child(7) > div:nth-child(2) > div.place_section > div.place_section_content > ul > li')

            # 리뷰 수가 0이 아닌 경우 리뷰 수집
            if len(review_lists) > 0:
                for j, review in enumerate(review_lists):
                    review_find = review.find('div:nth-of-type(3) > span:nth-of-type(2)')
                    if review_find is not None:
                        review_select = review.select('div:nth-of-type(3) > span:nth-of-type(2)')
                        review_select.click()
                        time.sleep(1)

                    self.review_list.append(
                        parse_review(review)
                    )
        except Exception as err:
            print(err)


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


def parse_review(review_dom: BeautifulSoup):

    # Todo xpath로 크롤링시 돔레벨이 다른 데이터들때문에 이슈, css selector로 처리시 돔 id가 계속 바뀜 .. 추후 다시 구현
    user_id = review_dom.select_one('div > a:nth-child(2) > div:nth-child(1)').text
    comment = review_dom.select_one('div:nth-child(2) > a > span').text
    temp = review_dom.select('.place_blind')
    date = temp[5].text
    score_dom = review_dom.select_one('li > div:nth-child(2)')
    score = '-1'
    if score_dom.text.strip():
        score = score_dom.text.strip()

    for each in score_dom.find_all('span'):
        each.decompose()

    each_review = {
        'user_id': user_id,
        'user_link': review_dom.select_one('div > a:nth-child(2)')['href'],
        'comment': comment,
        'score': score,
        'date': naver_date_formatter(date),
        'comment_id': hash(user_id + comment)
    }
    return each_review
