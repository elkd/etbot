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
from autopost.pages import LoginPage, clear_complete_profile_popup, clear_notif_popup
from autopost.tasks import run_upload


load_dotenv()

SCREENSHOT_PATH = env('SCREENSHOT_PATH')

def run_upload_task():
    post = ScheduledPost.objects.latest(
        'timestamp'
    )
    etuser = EtoroUser.objects.get(username='BAbylonFund')

    #with SmartDisplay() as disp:
    run_upload(post, etuser)

if __name__ == '__main__':
    run_upload_task()
