from media.base import ScrapBase
from utils.date_parser import *
from utils.http_request import Get


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

    def parse_html(self, text):
        pass

    def get_reviews(self):

        url = f'https://place.map.kakao.com/commentlist/v/{self.store_id}'
        review_list = []
        while True:
            get = Get(url, self.headers)
            data = get.request()
            comment = data['comment']
            has_next = comment['hasNext']
            list = comment['list']
            for each in range(list):
                comment_id = each['commentId']
                regdate = kakao_date_formatter(each['date'])
                if self.status == 'P' and not is_yesterday(regdate):
                    has_next = False
                    break

                if self.status == 's' and not is_two_years_before(regdate):
                    has_next = False
                    break

                review = {
                    'user_id': each['commentId'],
                    'user_link': 'https://map.kakao.com/?target=other&tab=review&mapuserid=' + each['commentId'],
                    'comment': each['contents'],
                    'score': each['point'],
                    'date': regdate,
                    'comment_id': comment_id,
                }
                review_list.append(review)
                url = f'https://place.map.kakao.com/commentlist/v/{self.store_id}/{comment_id}'

            if not has_next:
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
            open_time, off_time = make_manage_hour(api_place_info['openHour'])
            store_info = {
                'place_id': api_place_info['cid'],
                'description': api_place_info['description'],
                'name': api_place_info['placenamefull'],
                'geoX': api_place_info['wpointx'],
                'geoY': api_place_info['wpointy'],
                'address': api_place_info['address']['region']['fullname'] + ' ' + api_place_info['address']['addrbunho'],
                'roadAddress': api_place_info['address']['newaddr']['newaddrfull'],
                'phone': api_place_info['phonenum'],
                'keywords': api_place_info['category']['catename'].split(','),
                'thumbnail': api_place_info['mainphotourl'],
                'link': api_place_info['homepage'],
                'open_time': open_time,
                'off_time': off_time
            }

            return store_info
        except KeyError:
            # Todo 에러처리
            return
        pass

    def attach_headers(self, headers: dict) -> None:
        self.headers = headers


def make_manage_hour(place_json):
    if not place_json['openHour']:
        return '', ''

    open_hour = place_json['periodList']
    period_list = []
    if open_hour and len(open_hour) > 0:
        period_name = open_hour['periodName']
        time_list = open_hour["timeList"]
        for entry in time_list:
            time_name = entry.get("timeName", "")
            time_se = entry.get("timeSE", "")
            day_of_week = entry.get("dayOfWeek", "")
            result = f"{period_name} : {time_name} {time_se} {day_of_week}"
            period_list.append(result)

    off_hour = place_json['offdayList']
    off_day_list = []
    if off_hour and len(off_hour) > 0:
        for entry in time_list:
            time_name = entry.get("holidayName", "")
            time_se = entry.get("weekAndDay", "")
            result = f"{time_name} : {time_se}"
            off_day_list.append(result)

    return ','.join(period_list), ','.join(off_day_list)
