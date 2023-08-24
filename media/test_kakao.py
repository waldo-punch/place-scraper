from unittest import TestCase

from media.kakao import KakaoPlace


class TestKakaoPlace(TestCase):
    def test_get_place_basic_info(self):
        store_name = '울프강 스테이크 하우스'
        store_id = '26572124'
        status = 'P'
        store = KakaoPlace(store_id, store_name, status)
        info = store.get_place_basic_info()

        self.assertEqual(info['place_id'], '26572124')
        self.assertEqual(info['name'], '울프강스테이크하우스')
        self.assertEqual(info['address'], '서울 강남구 청담동 89-6')
        self.assertEqual(info['open_time'], '영업시간 : 11:00 ~ 22:00 매일')

    def test_get_reviews(self):
        store_name = '울프강 스테이크 하우스'
        store_id = '26572124'
        status = 'N'
        store = KakaoPlace(store_id, store_name, status)
        reviews = store.get_reviews()
        print(reviews, len(reviews))
