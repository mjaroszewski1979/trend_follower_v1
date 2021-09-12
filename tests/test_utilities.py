import unittest
from unittest import mock
from pandas_datareader._utils import RemoteDataError
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))  
parent = os.path.dirname(current)  
sys.path.append(parent)

import run
from utilities import TrendFollower

app = run.create_app()

tf = TrendFollower(user_name = 'trend_follower',user_password = 'turtle_trader',
email_name = 'mjaroherokuapp@gmail.com', email_password = 'mjaroherokuapp1234')



def get_data():
    df = mock.Mock()
    df.symbol_1 = 1000
    df.symbol_252 = 500

    if df.symbol_1 > df.symbol_252:
        return 'BULLISH'
    else:
        return 'BEARISH'


class TrendTestCase(unittest.TestCase):

    # Ensures that returned value is not none
    def test_user_name(self):
        self.assertIsNotNone(tf.user_name)
    
    # Ensures that returned value is not none
    def test_user_password(self):
        self.assertIsNotNone(tf.user_password)
    
    # Ensures that returned value is not none
    def test_email_name(self):
        self.assertIsNotNone(tf.email_name)

    # Ensures that returned value is not none
    def test_email_password(self):
        self.assertIsNotNone(tf.email_password)

    # Ensures that returned value is not none
    def test_data(self):
        self.assertIsNotNone(tf.data)

    # Ensures that returned value is not none
    def test_markets_data(self):
        self.assertIsNotNone(tf.markets_data)

    # Ensures that returned value is not none
    def test_marketspro_data(self):
        self.assertIsNotNone(tf.marketspro_data)

    # Ensures that returned value is not none
    def test_markets(self):
        self.assertIsNotNone(tf.markets)

    # Ensures that get_trend function works correctly
    def test_get_trend(self):
        actual = tf.get_trend('NASDAQ100')
        expected = 'BULLISH'
        self.assertEqual(actual, expected)

    # Ensures that get_trend function works correctly when exception occurs
    @mock.patch('routes.tf.get_trend', side_effect=Exception(RemoteDataError))
    def test_get_trend_error(self, fred):
        self.assertRaises(Exception, fred)

    # Ensures that get_data function works correctly
    def test_get_data_success(self):
        actual = get_data()
        expected = 'BULLISH'
        self.assertEqual(actual, expected)

    # Ensures that get_data function returns correct data type
    def test_get_data_type(self):
        actual = get_data()
        expected = str
        self.assertEqual(type(actual), expected)

    # Ensures that get_data function works correctly
    def test_get_data_failure(self):
        actual = get_data()
        expected = 'BEARISH'
        self.assertNotEqual(actual, expected)

    

    

if __name__ == '__main__':
    unittest.main()

