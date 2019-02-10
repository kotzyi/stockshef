import datetime


def get_today():
    return datetime.datetime.today()


def str_to_date(s):
    return datetime.datetime.strptime(s, '%Y%m%d')
