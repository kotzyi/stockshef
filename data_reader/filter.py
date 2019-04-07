import pandas as pd


class Filter:
    def __init__(self, dataframe):
        """
        Pandas dataframe에서 condition에 맞는 rows만 담겨있는 dataframe을 리턴하는 클래스
        """
        self.dataframe = dataframe

    def set_condition(self, expr):
        self.dataframe = self.dataframe.query(expr)

    def select(self, column_list):
        return self.dataframe[column_list]
