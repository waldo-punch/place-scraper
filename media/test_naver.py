from unittest import TestCase

from media.naver import NaverPlace


class TestNaverPlace(TestCase):
    def test_get_place_basic_info(self):
        store_name = '두껍삼 역삼직영점'
        store_id = '619673845'
        store = NaverPlace(store_id, store_name)
        print(store.get_place_basic_info())
