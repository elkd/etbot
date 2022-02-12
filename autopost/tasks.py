import os
import uuid
import traceback
from time import sleep

from celery import shared_task
from easyprocess import EasyProcess
from pyvirtualdisplay.smartdisplay import SmartDisplay
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
from .pages import LoginPage, clear_complete_profile_popup, clear_notif_popup
from autopost.models import ScheduledPost, EtoroUser, UploadReport


def login(browser, username=None, password=None, post=None):
    login_page = LoginPage(browser)

    if username is None and password is None:
        UploadReport.objects.create(
                post=post,
                notes=f'Uploading Failed, Username or Password is empty'
            )
        return None

    return login_page.login(username, password)


def start_browser(mode='simple'):
    if mode == 'human':
        options = uc.ChromeOptions()

        options.add_argument('--user-data-dir=ChromeBotProfile')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        browser = uc.Chrome(options=options, version_main=97)

        browser.implicitly_wait(30)
        # Lets open amazon in the first tab
        #browser.get('https://sell.amazon.com/beginners-guide')
        # Lets open https://www.bing.com/ in the second tab
        #browser.execute_script("window.open('about:blank', 'secondtab');")
        #browser.switch_to.window("secondtab")
        #browser.get('https://www.bing.com/')
        # Lets open https://www.facebook.com/ in the third tab
        #browser.execute_script("window.open('about:blank', 'thirdtab');")
        #browser.switch_to.window("thirdtab")
        browser.maximize_window()
        return browser
    else:
        options = uc.ChromeOptions()

        options.add_argument('--user-data-dir=ChromeBotProfile')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        browser = uc.Chrome(options=options, version_main=97)
        browser.implicitly_wait(30)
        browser.maximize_window()
        return browser


def upload_post(browser, post, retry=0):
    sleep(39)

    if post.content is None:
        UploadReport.objects.create(
                post=post,
                notes='Failed to Start the Upload process, Post content is empty'
            )
        return False

    try:
        wait = WebDriverWait(browser, 30)

        #open_postform_btn = wait.until(ec.presence_of_element_located((
        #    By.CSS_SELECTOR,
        #    'button.button-text.et-font-m'
        #)))
        open_postform_btn = browser.find_element_by_css_selector(
                'button.button-text.et-font-m'
            ) or browser.find_element_by_css_selector(
                    'a.write-new-post.sprite post'
                )
        open_postform_btn.click()

        UploadReport.objects.create(
                post=post,
                notes=f'Uploading in Progress, Etoro Upload Form is Opened...'
            )
        sleep(19)

        try:
            content_input = wait.until(ec.presence_of_element_located((
                By.CSS_SELECTOR,
                'textarea.write-post-textarea.ng-pristine.ng-valid.ng-touched'
            )))
            sleep(14)
            content_input.send_keys(post.content)

        except (
                UnexpectedAlertPresentException,
                NoSuchElementException,
                ElementNotInteractableException )  as e:

            UploadReport.objects.create(
                    post=post,
                    notes=f'Failed to Upload, known Exception captured: {traceback.format_exc()} Form is blocked, trying bypass...'
                )
            clear_complete_profile_popup(browser)

            sleep(16)
            #browser.execute_script("window.scrollBy(0,200)","")
            #wait.until_not(ec.visibility_of_element_located((By.ID, "cdk-overlay-0")))

        UploadReport.objects.create(
                post=post,
                notes=f'Uploading in Progress, Post Content has been pasted on the Etoro form...'
            )
        sleep(19)
        #content_input.send_keys(7 * Keys.BACKSPACE)

        if post.image is not None:
            UploadReport.objects.create(
                    post=post,
                    notes=f'Uploading in Progress, Fetching the post image: {post.image}'
                )
            upload_input = browser.find_element_by_class_name("form-upload-photo-label")
            sleep(4)
            upload_input.send_keys(post.image)
            sleep(34)

        wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "write-post-button"))).click()

        sleep(60)
        UploadReport.objects.create(
                post=post,
                notes=f'Successfully Uploaded the post On Etoro Website'
            )
        #browser.get('https://www.etoro.com/accounts/logout/')
    except TimeoutException as e:
        img = f'media/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
        browser.save_screenshot(img)
        UploadReport.objects.create(
                post=post,
                image=img,
                notes=f'Failed to Upload, Browser: {browser.title}, Windows Size: {browser.get_window_size()}, Exception: {traceback.format_exc()} Retrying...'
            )

        if retry < 3:
            retry+=1
            browser.refresh()
            #Etoro home has multiple windows object in an array eg windows[0] could be main or other
            #browser.execute_script("window.scrollBy(0,200)","")
            sleep(30)
            upload_post(browser, post, retry)

    except Exception as e:
        img = f'media/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
        browser.save_screenshot(img)
        UploadReport.objects.create(
                post=post,
                image=img,
                notes=f'Failed to Upload for Unknown reason, Title: {browser.title}, Cookies: {browser.get_cookies()}, Exception: {traceback.format_exc()}'
            )
        sleep(30)


@shared_task(bind=True, max_retries=3, default_retry_delay=10 * 60)
def post_task(self, postid=None):
    if postid is None:
        return None

    post = ScheduledPost.objects.get(id=postid)
    etuser = EtoroUser.objects.get(id=post.author.id)
    UploadReport.objects.create(
            post=post,
            notes='Starting the Uploading Process...'
        )

    with SmartDisplay() as disp:
        #img = disp.waitgrab()
        browser = start_browser(mode='human')
        UploadReport.objects.create(
                post=post,
                notes='Upload in progress, GUI browser has been opened and maximized'
            )

        res = title = None
        try:
            res, title = login(browser, etuser.username, etuser.password, post)
        except Exception as e:
            UploadReport.objects.create(
                    post=post,
                    notes='Login did not complete, possibly because the account is authenticated already!'
                )
            sleep(11)
            browser.get('https://etoro.com/home/')
            expected_title = ["eToro", "etoro"]

            if browser.title == "eToro":
                res = 'home'
            elif any(word in browser.title for word in expected_title):
                res = 'login'
            else:
                title = browser.title

        if res is not None:
            sleep(13)
            #browser.execute_script("window.scrollBy(0,300)", "")

            UploadReport.objects.create(
                    post=post,
                    notes=f'Logged In to account {etuser.username} successfully. Post creation is starting...'
                )

            try:
                upload_post(browser, post)
            except Exception as e:
                img = f'media/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
                browser.save_screenshot(img)
                UploadReport.objects.create(
                    post=post,
                    image=img,
                    notes=f'Failed to Complete the Upload, Celery will retry; Exception: {traceback.format_exc()}'
                )
                #https://hackernoon.com/using-celery-with-multiple-queues-retries-and-scheduled-tasks-589fe9a4f9ba
                self.retry(exc=e, countdown=180)  # the task goes back to the queue
        else:
            img = f'media/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
            browser.save_screenshot(img)
            UploadReport.objects.create(
                    post=post,
                    image=img,
                    notes=f'Failed to Login; Browser title is: {title}, Cookies are: browser.get_cookies()'
                )
        browser.close()
