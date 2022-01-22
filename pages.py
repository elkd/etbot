from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotInteractableException
)


def clear_complete_profile_popup(browser):
    try:
        # storing the current window handle to get back to dashboard
        main_page = browser.current_window_handle

        print(browser.window_handles)
        print(len(browser.window_handles))
        # changing the handles to access login page
        profile_page = None
        for handle in browser.window_handles:
            if handle != main_page:
                profile_page = handle

        # change the control to signin page       
        browser.switch_to.window(profile_page)

        pop_modal = WebDriverWait(browser, 60).until(ec.visibility_of_element_located((By.ID, "cdk-overlay-0")))

        #neverask_check = browser.find_element_by_css_selector('input#cbTradeModal')
        #browser.execute_script("arguments[0].click();", neverask_check)
        sleep(5)
        close_btn = browser.find_element_by_css_selector('button.default-font-icon.icon-close')
        browser.execute_script("arguments[0].click();", close_btn)

        sleep(5)
        #change control to main page
        browser.switch_to.window(main_page)
        return True
    except (NoSuchElementException, ElementNotInteractableException) as e:
        print(f'Clear Func has Exception {e}')
        sleep(5)
    return None


def clear_notif_popup(browser):
    try:
        # storing the current window handle to get back to dashboard
        main_page = browser.current_window_handle

        # changing the handles to access login page
        for handle in browser.window_handles:
            if handle != main_page:
                notif_page = handle

        # change the control to signin page       
        browser.switch_to.window(notif_page)

        close_btn = browser.find_element_by_css_selector('a.link.pre-push-popup-link')
        browser.execute_script("arguments[0].click();", close_btn)
        #change control to main page
        browser.switch_to.window(main_page)
        return True
    except NoSuchElementException as e:
        print(f'Clear Func has Exception {e}')
        sleep(5)
    return None


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

