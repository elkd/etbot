import os
from time import sleep

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException
)
from pages import LoginPage, clear_complete_profile_popup, clear_notif_popup


load_dotenv()

def login(browser):
    login_page = LoginPage(browser)

    username = os.getenv('ETOROUSER')
    password = os.getenv('ETOROPASSWORD')
    login_page.login(username, password)


def upload_post(browser):
    sleep(10)

    try:
        wait = WebDriverWait(browser, 90)

        open_postform_btn = wait.until(ec.visibility_of_element_located((
            By.CSS_SELECTOR,
            'button.button-text.et-font-m'
        )))
        open_postform_btn.click()

        sleep(10)
        content_input = wait.until(ec.visibility_of_element_located((
            By.CSS_SELECTOR,
            'textarea.write-post-textarea.ng-pristine.ng-valid.ng-touched'
        )))

        #content_input.send_keys(20 * Keys.BACKSPACE)
        content_input.send_keys('Here is the sample content')
        sleep(7)
        content_input.send_keys(7 * Keys.BACKSPACE)
        sleep(13)
        content_input.send_keys('is the content')
        sleep(14)
        upload_input = browser.find_element_by_class_name("form-upload-photo-label")
        upload_input.send_keys("./pics/sample.jpg")
        sleep(34)

        wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "write-post-button"))).click()

        sleep(60)
        print('hooray')
        print('hooray')
        #self.browser.get('https://www.etoro.com/accounts/logout/')

    except (
            TimeoutException,
            UnexpectedAlertPresentException,
            NoSuchElementException,
            ElementNotInteractableException )  as e:

        print(f'Eroto Known Exception Captured {e}')
        clear_complete_profile_popup(browser)

        sleep(10)
        browser.execute_script("window.scrollBy(0,200)","")
        #wait.until_not(ec.visibility_of_element_located((By.ID, "cdk-overlay-0")))
        upload_post(browser)

    except Exception as e:
        print(f'Unhandled Exception Happened: {e}')
        print(f'THE BROWSER WILL EXIT IN 60 SECONDS')
        print(f'THE BROWSER WILL EXIT SOONER...')
        browser.refresh()
        sleep(30)


def run_upload_task():
    options = uc.ChromeOptions()

    options.add_argument('--user-data-dir=ChromeBotProfile')
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')

    browser = uc.Chrome(options=options)
    browser.implicitly_wait(60)
    browser.maximize_window()

    #browser.get('https://etoro.com/home/')
    #try: browser.find_element_by_css_selector('home-element').click()
    #except NoSuchElementException as e: pass
    try:
        login(browser)
    except TimeoutException as e:
        sleep(30)
        login(browser)
        print(e)

    browser.execute_script("window.scrollBy(0,300)","")
    upload_post(browser)
    browser.close()


if __name__ == '__main__':
    run_upload_task()