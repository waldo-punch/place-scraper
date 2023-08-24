import logging
import time

from media.base import ScrapBase
from utils.date_parser import *
from utils.http_request import Get

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class KakaoPlace(ScrapBase):
    headers = {
        'User-Agent': 'Mozilla',
        'content-type': 'application/json',
    }

    def __init__(self, store_id: str, store_name: str, status: str):
        self.store_id = store_id
        self.store_name = store_name

        # N : 신규, P : 수집중, E : 수집 종료
        self.status = status
        self.store_info = {}
        self.review_list = []

    def run(self):
        self.store_info = self.get_place_basic_info()
        self.review_list.append(self.get_reviews())

    def parse_html(self, text):
        pass

    def get_reviews(self):
        url = f'https://place.map.kakao.com/commentlist/v/{self.store_id}'
        review_list = []
        while True:
            print(url)
            get = Get(url, self.headers)
            data = get.request()
            try:
                comment = data.get('comment')
                has_next = comment.get('hasNext')
                list = comment.get('list')
                for each in list:
                    comment_id = each.get('commentid')
                    regdate = kakao_date_formatter(each.get('date'))
                    if self.status == 'P' and not is_yesterday(regdate):
                        has_next = False
                        break

                    if self.status == 'N' and not is_two_years_before(regdate):
                        has_next = False
                        break

                    review = {
                        'user_id': each.get('commentid'),
                        'user_link': 'https://map.kakao.com/?target=other&tab=review&mapuserid=' + each['commentid'],
                        'comment': each.get('contents',''),
                        'score': each.get('point',''),
                        'date': regdate,
                        'comment_id': comment_id,
                    }
                    review_list.append(review)
                    url = f'https://place.map.kakao.com/commentlist/v/{self.store_id}/{comment_id}'

                if not has_next:
                    break
                time.sleep(0.3)
            except KeyError as e:
                logger.error(f"Error parsing data: {e}")
                break

        return review_list

    def get_comments(self):
        pass

    def get_place_basic_info(self):
        url = f'https://place.map.kakao.com/main/v/{self.store_id}'
        try:
            get = Get(url, self.headers)
            data = get.request()
            api_place_info = data['basicInfo']
            open_time = make_manage_hour(api_place_info)
            store_info = {
                'place_id': str(api_place_info['cid']),
                'name': api_place_info['placenamefull'],
                'geoX': api_place_info['wpointx'],
                'geoY': api_place_info['wpointy'],
                'address': api_place_info['address']['region']['fullname'] + ' ' + api_place_info['address'][
                    'addrbunho'],
                'roadAddress': api_place_info['address']['newaddr']['newaddrfull'],
                'phone': api_place_info['phonenum'],
                'keywords': api_place_info['category']['catename'].split(','),
                'thumbnail': api_place_info['mainphotourl'],
                'link': api_place_info['homepage'],
                'open_time': open_time
            }

            return store_info
        except KeyError as e:
            logger.error(f"Error getting place basic info: {e}")
            return
        pass

    def attach_headers(self, headers: dict) -> None:
        self.headers = headers


def make_manage_hour(place_json):
    open_hour = place_json.get('openHour', '')
    manage_list = []
    if open_hour and len(open_hour) > 0:
        realtime = open_hour.get('realtime', '')
        period = realtime.get('currentPeriod', '')
        if period and len(period) > 0:
            time_list = period["timeList"]
            for entry in time_list:
                time_name = entry.get("timeName", "")
                time_se = entry.get("timeSE", "")
                day_of_week = entry.get("dayOfWeek", "")
                result = f"{time_name} : {time_se} {day_of_week}"
                manage_list.append(result)

    return ','.join(manage_list)
