import unittest
import win32com
from reader import CreonAPI


class CreonAPITest(unittest.TestCase):
    api = CreonAPI

    def test_login_the_api_server(self):
        login = CreonAPITest.api.login()
        self.asserEqual(login, self.api.OK)

    def test_connect_the_api_server(self):
        connect = CreonAPITest.api.connect()
        self.assertEqual(connect, self.api.OK)

    def test_get_stock_chart(self):
        pass

    def test_get_stock_list(self):
        stock_lists = CreonAPITest.api.get_stock_list()

        self.assertIsNotNone(stock_lists['kospi'])
        self.assertIsNotNone(stock_lists['kosdaq'])

    def test_watch_stock_chart(self):
        pass


if __name__ == '__main__':
    unittest.main(warnings='ignore')
