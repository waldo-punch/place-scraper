from unittest import TestCase

from utils.date_parser import *


class Test(TestCase):
    def test_extract_recent_dates(self):
        test1 = naver_date_formatter("2023년 8월 21일 월요일")
        test2 = naver_date_formatter("2021년 5월 11일 수요일")
        self.assertTrue(is_two_years_before(test1))
        self.assertFalse(is_two_years_before(test2))

    def test_kakao_date_formatter(self):
        date = "2023.07.25."
        print(kakao_date_formatter(date))

    def test_is_yesterday(self):
        test1 = naver_date_formatter("2023년 8월 24일 월요일")
        test2 = naver_date_formatter("2021년 5월 11일 수요일")
        test3 = kakao_date_formatter("2023.07.25.")

        self.assertTrue(is_yesterday(test1))
        self.assertFalse(is_yesterday(test2))
        self.assertFalse(is_yesterday(test3))
        self.assertTrue(is_two_years_before(test3))
