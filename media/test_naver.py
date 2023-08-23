from unittest import TestCase

from bs4 import BeautifulSoup

from media.naver import NaverPlace, parse_review


class TestNaverPlace(TestCase):
    def test_get_place_basic_info(self):
        store_name = '두껍삼 역삼직영점'
        store_id = '619673845'
        status = 'P'
        store = NaverPlace(store_id, store_name, status)
        print(store.get_place_basic_info())

    def test_get_reviews(self):
        store_name = '두껍삼 역삼직영점'
        store_id = '619673845'
        store = NaverPlace(store_id, store_name, 'P')
        store.get_reviews()

    def test_parsing_html(self):
        try:
            f = open("../test/naver_review.txt", 'r')
            data = f.read()

            bs = BeautifulSoup(data, 'html.parser')
            review = parse_review(bs)
            self.assertEqual(review['user_id'], '맛집세계여행')
            self.assertEqual(review['comment'], '고기의 육즙도 좋고 후식 된장도 맛있네요')
            self.assertEqual(review['score'], '5')
        except Exception as err:
            print(err)
            pass
        finally:
            f.close()
