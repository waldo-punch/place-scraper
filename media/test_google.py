from unittest import TestCase

from media.google import GooglePlace

class TestGooglePlace(TestCase):
    def test_get_place_basic_info(self):
        store_name = '두껍삼 역삼직영점'
        store_id = '서울특별시 강남구 역삼1동 테헤란로8길 두껍삼 역삼직영점'
        status = 'N'
        store = GooglePlace(store_id, store_name, status)
        print(store.get_place_basic_info())

    def test_get_review(self):
        store_name = '두껍삼 역삼직영점'
        store_id = '서울특별시 강남구 역삼1동 테헤란로8길 두껍삼 역삼직영점'
        status = 'N'
        store = GooglePlace(store_id, store_name, status)
        store.get_reviews()
