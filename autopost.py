import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
import undetected_chromedriver as uc

from pages import LoginPage

load_dotenv()



def login():
    #browser = webdriver.Firefox()
    #browser = webdriver.Chrome()
    browser = uc.Chrome()
    browser.implicitly_wait(5)

    login_page = LoginPage(browser)

    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')
    login_page.login(username, password)

    try:
        errors = browser.find_elements_by_css_selector('#error_message')
    except Exception as e:
        print(f'Cannot catch Errors: {e}')
    sleep(300)
    browser.close()

if __name__ == '__main__':
    login()
