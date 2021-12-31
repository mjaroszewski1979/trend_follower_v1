from selenium.webdriver.support.ui import WebDriverWait as W
from selenium.webdriver.support import expected_conditions as EC
from locators import HomePageLocators, LoginPageLocators, RegisterPageLocators



class BasePage(object):


    def __init__(self, driver):
        self.driver = driver

    def do_click(self, locator):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).click()

    def do_clear(self, locator):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).clear()

    def do_send_keys(self, locator, text):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).send_keys(text)

    def get_element(self, locator):
        element = W(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element

    def get_elements(self, locator):
        elements = W(self.driver, 10).until(EC.visibility_of_all_elements_located(locator))
        return elements

    def get_element_text(self, locator):
        element = W(self.driver, 10).until(EC.visibility_of_element_located(locator))
        return element.text

    def do_submit(self, locator):
        W(self.driver, 10).until(EC.visibility_of_element_located(locator)).submit()


class HomePage(BasePage):

    def is_title_matches(self):
        return "Home - Trend Follower" in self.driver.title

    def is_register_link_works(self):
        self.do_click(HomePageLocators.REGISTER_LINK)
        return "Register - Trend Follower" in self.driver.title

    def is_login_link_works(self):
        self.do_click(HomePageLocators.LOGIN_LINK)
        return "Login - Trend Follower" in self.driver.title

    def is_home_link_works(self):
        self.do_click(HomePageLocators.HOME_LINK)
        return "Home - Trend Follower" in self.driver.title

    def is_adding_markets_works(self):
        self.do_click(HomePageLocators.SELECTION)
        self.do_click(HomePageLocators.BTN_SEL)
        msg = self.get_element_text(HomePageLocators.MSG_TEXT)
        return 'MARKET ADDED. BECOME A PRO MEMBER AND GET ACCESS TO MORE FINANCIAL INSTRUMENTS!' in msg

    def is_delete_link_works(self):
        buttons_before = self.get_elements(HomePageLocators.DELETE_LINK)
        buttons_before_qt = len(buttons_before)
        delete_button = buttons_before[0]
        delete_button.click()
        buttons_after_qt = len(self.get_elements(HomePageLocators.DELETE_LINK))
        return (buttons_before_qt - 1) == buttons_after_qt


class LoginPage(BasePage):

    def is_title_matches(self):
        return "Login - Trend Follower" in self.driver.title

    def is_login_form_works(self):
        self.do_clear(LoginPageLocators.NAME)
        self.do_clear(LoginPageLocators.PASSWORD)
        self.do_send_keys(LoginPageLocators.NAME, 'trend_follower')
        self.do_send_keys(LoginPageLocators.PASSWORD, 'turtle_trader')
        self.do_submit(LoginPageLocators.PASSWORD)
        logout = self.get_element_text(LoginPageLocators.LOGOUT_LINK)
        return 'LOGOUT' in logout

    def is_logout_link_works(self):
        self.do_click(LoginPageLocators.LOGOUT_LINK)
        logout_msg = self.get_element_text(LoginPageLocators.LOGOUT_MSG)
        return 'YOU HAVE BEEN LOGGED OUT!' in logout_msg

class RegisterPage(BasePage):

    def is_title_matches(self):
        return "Register - Trend Follower" in self.driver.title

    def is_register_form_works(self):
        self.do_clear(RegisterPageLocators.REG_NAME)
        self.do_clear(RegisterPageLocators.REG_EMAIL)
        self.do_send_keys(RegisterPageLocators.REG_NAME, 'maciej')
        self.do_send_keys(RegisterPageLocators.REG_EMAIL, 'mj@gmail.com')
        self.do_submit(RegisterPageLocators.REG_EMAIL)
        return "Login - Trend Follower" in self.driver.title 





   