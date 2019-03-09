import datetime
import pandas as pd


def get_today():
    return datetime.datetime.today()


def date_to_str(date):
    return date.strftime('%Y%m%d')


def str_to_date(s, fmt='%Y%m%d'):
    return datetime.datetime.strptime(s, fmt)


def get_open_time():
    return pd.DataFrame(pd.date_range("09:01", "15:30", freq="1min").strftime('%H%M'))