from abc import *


class ScrapBase(metaclass=ABCMeta):
    @abstractmethod
    def get_reviews(self, place_id: str):
        pass

    @abstractmethod
    def get_comments(self, place_id: str):
        pass

    @abstractmethod
    def get_place_basic_info(self, place_id: str):
        pass

    @abstractmethod
    def parse_html(self, text):
        pass