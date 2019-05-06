import util
import os
from filter import Filter


def main():
    today = util.date_to_str(util.get_today())
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data/info/{}.csv'.format(today))

    company_info = util.get_csv(file_path)

    filter = Filter(company_info)


    expr = ''
    filter.set_condition()

def filter_by_market_watch():

def filter_by_stock_header():


if __name__== '__main__':
    main()
