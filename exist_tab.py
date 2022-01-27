#Run on Existing browser
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import (
    NoSuchElementException, ElementNotInteractableException
)


options = webdriver.ChromeOptions()
options.add_experimental_option('debuggerAddress', 'localhost:9222')
browser = webdriver.Chrome(options=options)

browser.implicitly_wait(10)

print('Starting...')
sleep(5)


#shadow_host = browser.find_element(By.CLASS_NAME, 'ng-star-inserted')
#shadow_root = shadow_host.shadow_root
#shadow_content = shadow_root.find_element(By.CSS_SELECTOR, 'button.default-font-icon.icon-close')
#shadow_content.click()

#/html/body/div[9]/div[2]/div
#change control to main page
#browser.switch_to.window(main_page)
#browser.switchTo().defaultContent()


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
