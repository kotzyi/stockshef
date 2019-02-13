import datetime


def get_today():
    return datetime.datetime.today()


def date_to_str(date):
    return date.strftime('%Y%m%d')


def str_to_date(s):
    return datetime.datetime.strptime(s, '%Y%m%d')
