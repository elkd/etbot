import os
import uuid
import traceback
from time import sleep

from selenium.common.exceptions import (
    UnexpectedAlertPresentException,
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException
)
from pyvirtualdisplay.smartdisplay import SmartDisplay
from celery import shared_task
from etbot.settings import env
from .pages import LoginPage, clear_complete_profile_popup, clear_notif_popup
from autopost.models import ScheduledPost, EtoroUser, UploadReport


MEDIA_PATH = env('MEDIA_PATH')

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
        try:
            run_upload(post, etuser)
        except Exception as e:
            img = f'{MEDIA_PATH}/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
            #browser.save_screenshot(img)
            UploadReport.objects.create(
                post=post,
                notes=f'Failed to Complete the Upload, Celery will retry; Exception: {traceback.format_exc()}'
            )
            self.retry(exc=e, countdown=180)  # the task goes back to the queue


def login(browser, username=None, password=None, post=None, timeout=50):
    login_page = LoginPage(browser, timeout)

    if login_page.success is False:
        return None, f'Login Page Failed to load in Time: {timeout} Seconds'

    if username is None or password is None:
        UploadReport.objects.create(
                post=post,
                notes=f'Login Failed, Username or Password is empty'
            )
        return None, 'Username or Password is Empty'

    return login_page.login(username, password)


def start_browser(mode='simple'):
    import undetected_chromedriver as uc
    if mode == 'human':
        options = uc.ChromeOptions()

        options.add_argument('--user-data-dir=ChromeBotProfile')
        options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
        browser = uc.Chrome(options=options, version_main=env('CHROME_VERSION'))

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
        browser = uc.Chrome(options=options, version_main=env('CHROME_VERSION'))
        browser.implicitly_wait(30)
        browser.maximize_window()
        return browser


def upload_post(browser, post, retry=0):
    from selenium.webdriver.support.ui import WebDriverWait
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
            content_input = browser.switch_to.active_element
            #wait.until(ec.presence_of_element_located((
            #    By.CSS_SELECTOR,
            #    'textarea.write-post-textarea.ng-pristine.ng-valid.ng-touched'
            #)))
            content_input.clear()
            sleep(9)
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
        #write_post_wrapper= content_input.find_element_by_xpath(".//ancestor::div[@class='write-post-wrapper']")
        write_post_wrapper = content_input.find_element_by_xpath('./../../../../..')
        print(f'Parent Class which is post wrapper is: {write_post_wrapper.get_attribute("class")}')

        if post.image is not None:
            UploadReport.objects.create(
                    post=post,
                    notes=f'Uploading in Progress, Fetching the post image: {post.image}'
                )

            #//*[@id="cdk-overlay-1"]/et-dialog-container/et-modal/div/div[3]/div/et-form-attachment-upload/div/input
            upload_input = write_post_wrapper.find_element_by_name("photo")
            sleep(4)
            upload_input.send_keys(post.image.path)
            sleep(53)

        write_post_wrapper.find_element_by_class_name('write-post-button').click()
        #wait.until(ec.element_to_be_clickable((By.CLASS_NAME, "")))

        sleep(13)
        UploadReport.objects.create(
                post=post,
                notes=f'Successfully Uploaded the post On Etoro Website'
            )
        #browser.get('https://www.etoro.com/accounts/logout/')
    except TimeoutException as e:
        img = f'{MEDIA_PATH}/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
        #browser.save_screenshot(img)
        UploadReport.objects.create(
                post=post,
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
        img = f'{MEDIA_PATH}/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
        #browser.save_screenshot(img)
        UploadReport.objects.create(
                post=post,
                notes=f'Failed to Upload for Unknown reason, Title: {browser.title}, Cookies: {browser.get_cookies()}, Exception: {traceback.format_exc()}'
            )
        sleep(30)


def run_upload(post, etuser):
    try:
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
                    notes='Login did not complete; Exception: {traceback.format_exc()}, Returned Msg: {title}'
                )

        if str(browser.current_url).endswith('home') or browser.title == "eToro":
            res = browser.title

        if res is not None:
            sleep(13)

            UploadReport.objects.create(
                    post=post,
                    notes=f'Logged In to account {etuser.username} successfully. Post creation is starting...'
                )

            upload_post(browser, post)
        else:
            img = f'{MEDIA_PATH}/images/uploaderror/{post.slug}-{uuid.uuid4().hex[:6]}.png'
            #browser.save_screenshot(img)
            UploadReport.objects.create(
                    post=post,
                    notes=f'Failed to Login; Browser title is: {title}, Cookies are: {browser.get_cookies()}'
                )
    finally:
        browser.close()
