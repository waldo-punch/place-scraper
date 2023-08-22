from media.base import ScrapBase


class NaverPlace(ScrapBase):

    def get_reviews(self, place_id: str):
        pass

    def get_comments(self, place_id: str):
        pass

    def get_place_basic_info(self, place_id: str):
        pass

    def parse_html(self, text):
        pass
