import unittest
import re
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))  
parent = os.path.dirname(current)  
sys.path.append(parent)

import run

app = run.create_app()




class RoutesTestCase(unittest.TestCase):


    # Ensures that the application instance exists
    def test_app_exists(self):
        self.assertIsNotNone(app)

    # Ensures that index page loads correctly
    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensures that the data returned contains actual text from the index page
    def test_index_data(self):
        tester = app.test_client(self)
        response = tester.get('/', content_type='html/text')
        self.assertTrue(b'SELECT YOUR MARKET:' in response.data)

    # Ensures that submitting form on the index page works correctly
    def test_index_post(self):
        tester = app.test_client(self)
        response = tester.post('/', data=dict(name='S&P 500'), follow_redirects=True)
        self.assertTrue(re.search('MARKET ADDED', response.get_data(as_text=True)))

    # Ensures that login page loads correctly
    def test_login(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensures that the data returned contains actual text from the login page
    def test_login_data(self):
        tester = app.test_client(self)
        response = tester.get('/login', content_type='html/text')
        self.assertTrue(b'PLEASE ENTER NAME' in response.data)

    # Ensures that login mechanism behaves as expected when provided with correct credentials
    def test_login_success(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(name='trend_follower', password='turtle_trader'), follow_redirects=True)
        response = tester.get('/pro', content_type='html/text')
        self.assertIn(b'PRO', response.data)

    # Ensures that login mechanism behaves as expected when provided with incorrect credentials
    def test_login_failure(self):
        tester = app.test_client(self)
        response = tester.post('/login', data=dict(name='wrong_name', password='wrong_password'), follow_redirects=True)
        self.assertTrue(re.search('WRONG NAME OR PASSWORD!', response.get_data(as_text=True)))
        
    # Ensures that logout page is working correctly
    def test_logout(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(name='trend_follower', password='turtle_trader'), follow_redirects=True)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'YOU HAVE BEEN LOGGED OUT!', response.data)

    # Ensures that logout page is available only to authorized users
    def test_logout_unauthorized(self):
        tester = app.test_client(self)
        response = tester.get('/logout', follow_redirects=True)
        self.assertIn(b'Unauthorized  - Trend Follower', response.data)

    # Ensures that pro page returns correct status code after successful login
    def test_pro(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(name='trend_follower', password='turtle_trader'), follow_redirects=True)
        response = tester.get('/pro', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensures that pro page behaves as expected after successful form submission 
    def test_pro_post(self):
        tester = app.test_client(self)
        tester.post('/login', data=dict(name='trend_follower', password='turtle_trader'), follow_redirects=True)
        tester.post('/pro', data=dict(name='US DOLLAR'), follow_redirects=True)
        response = tester.get('/pro', content_type='html/text')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'US DOLLAR', response.data)

    # Ensures that pro page is available only to authorized users
    def test_pro_unauthorized(self):
        tester = app.test_client(self)
        response = tester.get('/pro', follow_redirects=True)
        self.assertIn(b'Unauthorized  - Trend Follower', response.data)

    # Ensures that register page loads correctly
    def test_register(self):
        tester = app.test_client(self)
        response = tester.get('/register', content_type='html/text')
        self.assertEqual(response.status_code, 200)

    # Ensures that the data returned contains actual text from the register page
    def test_register_data(self):
        tester = app.test_client(self)
        response = tester.get('/register', follow_redirects=True, content_type='html/text')
        self.assertTrue(b'PLEASE ENTER EMAIL' in response.data)

    # Ensures that register page flashes correct message after successful form submission
    def test_register_post(self):
        tester = app.test_client(self)
        response = tester.post('/register', data=dict(name='maciej', email='maciej@gmail.com'), follow_redirects=True)
        self.assertTrue(re.search('THANK YOU. PLEASE CHECK YOUR EMAIL!', response.get_data(as_text=True)))

     # Ensures that error/404 page loads correctly
    def test_404(self):
        tester = app.test_client(self)
        response = tester.get('/404', content_type='html/text')
        self.assertEqual(response.status_code, 404)

    # Ensures that the data returned contains actual text from the error/404 page
    def test_404_data(self):
        tester = app.test_client(self)
        response = tester.get('/404', content_type='html/text')
        self.assertTrue(b'THE WEBSITE YOU WERE LOOKING FOR.' in response.data)


if __name__ == '__main__':
    unittest.main()