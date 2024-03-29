from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotInteractableException
)


def clear_complete_profile_popup(browser):
    try:
        sleep(5)

        #complete_prof_popup = browser.find_element_by_css_selector("div#cdk-overlay-1")
        #ActionChains(browser).move_to_element(complete_prof_popup).pause(1).click(complete_prof_popup).perform()


        #close_btn = browser.find_element_by_xpath('//*[@id="cdk-overlay-1"]/et-dialog-container/et-post-verification/div/div[2]/div[1]/a')
        #browser.switch_to().activeElement()
        #WebDriverWait.until(ec.visibility_of_element_located((
        #    By.XPATH,
        #    "/html/body/div[6]/div[2]/div/et-dialog-container/et-post-verification/div/div[2]/div[1]/a"
        #)));

        close_btn = browser.find_element_by_xpath('/html/body/div[6]/div[2]/div/et-dialog-container/et-post-verification/div/div[2]/div[1]/a')

        browser.execute_script("arguments[0].click();", close_btn)

        sleep(5)
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
    def __init__(self, browser, timeout):
        self.browser = browser
        self.success = False
        #Login page loads a lot of unnecessary static files, so ignore that
        try:
            self.browser.set_page_load_timeout(timeout)
            self.browser.get('https://www.etoro.com/login/')
            self.success = True
        except:
            try:
                wait.until(ec.presence_of_element_located((
                    By.ID, 'username'
                )))
                self.success = True
            except:
                print('there is no Element with ID username on the Login page')
                self.success = False


    def login(self, username, password):
        sleep(8)
        expected_title = ["eToro", "Login", "Various Ways", "Sign Into", "Your Account"]

        if not any(word in self.browser.title for word in expected_title):
            return None, self.browser.title

        username_input = self.browser.find_element_by_id("username") or self.browser.find_element_by_css_selector("input[name='username']")
        password_input = self.browser.find_element_by_id("password") or self.browser.find_element_by_css_selector("input[name='password']")

        username_input.clear()
        sleep(12)
        username_input.send_keys(username)

        sleep(11)
        password_input.clear()
        sleep(4)
        password_input.send_keys(password)
        sleep(9)
        login_button = self.browser.find_element_by_xpath("//button[@class='button-default blue-btn']")
        login_button.click()
        sleep(5)
        return True, self.browser.title


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

