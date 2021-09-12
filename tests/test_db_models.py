import unittest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))  
parent = os.path.dirname(current)  
sys.path.append(parent)

import run
from models import User, Markets, MarketsPro
from extensions import db


app = run.create_app()
app.config['TESTING'] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db.init_app(app)
app.app_context().push() 
user = User()


class RoutesTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()
        user.is_authenticated == True

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        user.is_authenticated == False

    # Ensures that data base model Market is working correctly
    def test_db_markets(self):
        new_market = Markets(name='SP500', symbol='S&P 500', trend='BULLISH')
        db.session.add(new_market)
        db.session.commit()
        existing_market = Markets.query.filter_by(name='SP500').first()
        self.assertEqual(existing_market.trend, 'BULLISH')

    # Ensures that data base model MarketPro is working correctly
    def test_db_markets_pro(self):
        new_market = MarketsPro(name='BITCOIN', symbol='CBBTCUSD', trend='BEARISH')
        db.session.add(new_market)
        db.session.commit()
        existing_market = MarketsPro.query.filter_by(name='BITCOIN').first()
        self.assertEqual(existing_market.symbol, 'CBBTCUSD')

    # Ensures that delete mechanism works as expected
    def test_delete(self):
        new_market = Markets(name='SP500', symbol='S&P 500', trend='BULLISH')
        db.session.add(new_market)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.delete('/delete/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"BULLISH", response.data)

    # Ensures that update mechanism works as expected
    def test_update(self):
        new_market = Markets(name='SP500', symbol='S&P 500', trend='BULLISH')
        db.session.add(new_market)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.patch('/update/1', data=dict(trend='BEARISH'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"BULLISH", response.data)

    # Ensures that delete mechanism works as expected for authorized users
    def test_delete_pro(self):
        new_market = Markets(name='SP500', symbol='S&P 500', trend='BULLISH')
        db.session.add(new_market)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.delete('/delete_pro/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"BULLISH", response.data)

    # Ensures that update mechanism works as expected for authorized users
    def test_update_pro(self):
        new_market = Markets(name='SP500', symbol='S&P 500', trend='BULLISH')
        db.session.add(new_market)
        db.session.commit()
        tester = app.test_client(self)
        response = tester.patch('/update_pro/1', data=dict(trend='BEARISH'), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"BULLISH", response.data)





  


if __name__ == '__main__':
    unittest.main()