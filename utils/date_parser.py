from datetime import datetime, timedelta


def is_two_years_before(date_str):
    current_date = datetime.now()
    two_years_ago = current_date - timedelta(days=365 * 2)

    try:
        date_obj = naver_date_formatter(date_str)
        if two_years_ago <= date_obj:
            return True
    except ValueError:
        pass

    return False


def is_yesterday(date_str):
    current_date = datetime.now()
    two_years_ago = current_date - timedelta(days=1)

    try:
        date_obj = naver_date_formatter(date_str)
        if two_years_ago <= date_obj:
            return True
    except ValueError:
        pass

    return False


def naver_date_formatter(date_str):
    formatted_date = date_str[0:-4]
    date_obj = datetime.strptime(formatted_date, '%Y년 %m월 %d일')
    return date_obj
