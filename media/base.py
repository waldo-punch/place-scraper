from abc import *


class ScrapBase(metaclass=ABCMeta):
    @abstractmethod
    def get_reviews(self):
        pass

    @abstractmethod
    def get_comments(self):
        pass

    @abstractmethod
    def get_place_basic_info(self):
        pass

    @abstractmethod
    def parse_html(self, text):
        pass