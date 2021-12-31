import sys
import os

current = os.path.dirname(os.path.realpath(__file__)) 
parent = os.path.dirname(current)
sys.path.append(parent)

from selenium import webdriver
import page
from run import create_app
import unittest



class TestBase(unittest.TestCase):


    def setUp(self):
        app = create_app()
        app.app_context().push()
        self.driver =  webdriver.Chrome('chromedriver.exe')
        self.driver.set_window_size(1920, 1080)


    def tearDown(self):
        self.driver.close()


class SeleniumTest(TestBase):
        
    def test_home_page(self):
        self.driver.get('http://127.0.0.1:5000/')
        home_page = page.HomePage(self.driver)
        assert home_page.is_title_matches()
        assert home_page.is_login_link_works()
        assert home_page.is_register_link_works()
        assert home_page.is_home_link_works()
        assert home_page.is_adding_markets_works()
        assert home_page.is_delete_link_works()


    def test_login_page(self):
        self.driver.get('http://127.0.0.1:5000/login')
        login_page = page.LoginPage(self.driver)
        assert login_page.is_title_matches()
        assert login_page.is_login_form_works()
        assert login_page.is_logout_link_works()

    def test_register_page(self):
        self.driver.get('http://127.0.0.1:5000/register')
        register_page = page.RegisterPage(self.driver)
        assert register_page.is_title_matches()
        assert register_page.is_register_form_works()


if __name__ == '__main__':
    unittest.main()


        