from time import sleep
from selenium.webdriver.common.keys import Keys


class LoginPage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.etoro.com/login/')

    def login(self, username, password):
        try:
            username_input = self.browser.find_element_by_id("username") or self.browser.find_element_by_css_selector("input[name='username']")
            password_input = self.browser.find_element_by_id("password") or self.browser.find_element_by_css_selector("input[name='password']")

            username_input.send_keys(20 * Keys.BACKSPACE)
            username_input.send_keys(username)
            sleep(5)
            #password_input.send_keys(20 * Keys.BACKSPACE)
            password_input.send_keys(password)
            sleep(5)
            login_button = self.browser.find_element_by_xpath("//button[@class='button-default blue-btn']")
            login_button.click()
            sleep(5)
        except Exception as e:
            print(f'Could not Login: {e}')


class HomePage:
    def __init__(self, browser):
        self.browser = browser
        self.browser.get('https://www.etoro.com/')

    def go_to_login_page(self):
        try:
            self.browser.find_element_by_xpath("//a[text()='Login']").click()
            sleep(2)
            return LoginPage(self.browser)
        except Exception as e:
            print(f'Could not Click Login: {e}')

