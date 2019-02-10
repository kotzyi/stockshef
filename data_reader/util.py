import datetime
import os


def get_today(fmt='%Y%m%d'):
    return datetime.datetime.today().strftime(fmt)


def create_file(filepath):
    basedir = os.path.dirname(filepath)
    if not os.path.exists(basedir):
        os.makedirs(basedir)

    if not os.path.isfile(filepath):
        open(filepath, 'a').close()


def str_to_date(s):
    return datetime.datetime.strptime(s, '%Y%m%d')
