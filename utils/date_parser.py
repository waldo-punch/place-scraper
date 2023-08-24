from datetime import datetime, timedelta


def is_two_years_before(date_param):
    current_date = datetime.now()
    two_years_ago = current_date - timedelta(days=365 * 2)

    if two_years_ago <= date_param:
        return True

    return False


def is_yesterday(date_param):
    current_date = datetime.now()
    day_before = current_date - timedelta(days=1)

    if day_before <= date_param:
        return True

    return False


def naver_date_formatter(date_str):
    formatted_date = date_str[0:-4]
    date_obj = datetime.strptime(formatted_date, '%Y년 %m월 %d일')
    return date_obj


def kakao_date_formatter(date_str):
    date_obj = datetime.strptime(date_str, '%Y.%m.%d.')
    return date_obj


def get_now():
    return datetime.now()