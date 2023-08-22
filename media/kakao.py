from media.base import ScrapBase


class KakaoPlace(ScrapBase):
    def parse_html(self, text):
        pass

    def get_reviews(self, place_id: str):
        pass

    def get_comments(self, place_id: str):
        pass

    def get_place_basic_info(self, place_id: str):
        pass