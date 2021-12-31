from selenium.webdriver.common.by import By

class HomePageLocators(object):

    REGISTER_LINK = (By.CLASS_NAME, 'register-link')
    LOGIN_LINK = (By.CLASS_NAME, 'login-link')
    HOME_LINK = (By.CLASS_NAME, 'home-link')
    DELETE_LINK = (By.CLASS_NAME, 'delete-btn')
    SELECTION = (By.XPATH, "//select/option[@value='GOLD']")
    BTN_SEL = (By.ID, 'btn-sel')
    MSG_TEXT = (By.CLASS_NAME, 'msg-text')

class LoginPageLocators(object):

    NAME = (By.NAME, 'name')
    PASSWORD = (By.NAME, 'password')
    LOGOUT_LINK = (By.CLASS_NAME, 'logout-link')
    LOGOUT_MSG = (By.CLASS_NAME, 'logout-msg')

class RegisterPageLocators(object):

    REG_NAME = (By.NAME, 'name')
    REG_EMAIL = (By.NAME, 'email')




