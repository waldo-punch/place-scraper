from unittest import TestCase

from utils.date_parser import is_two_years_before


class Test(TestCase):
    def test_extract_recent_dates(self):

        self.assertTrue(is_two_years_before("2023년 8월 21일 월요일"))
        self.assertFalse(is_two_years_before("2021년 5월 11일 수요일"))

