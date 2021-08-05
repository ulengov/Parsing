from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from pymongo import MongoClient
import time

def _parse_element(element, css_selector):
    result = WebDriverWait(element, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, css_selector))).text
    return result

def parse_email(element):

    from_name = _parse_element(
        element, 'span[class~="ns-view-message-head-sender-name"]')
    from_email = _parse_element(
        element, 'span[class~="mail-Message-Sender-Email"]')
    date = _parse_element(
        element, 'div[class~="ns-view-message-head-date"]')
    subject = _parse_element(
        element, 'div[class~="mail-Message-Toolbar-Subject"]')
    text_messege = _parse_element(
        element, 'div.mail-Message-Body-Content')

    item = {
        'from_name': from_name, \
        'from_email': from_email, \
        'date': date, \
        'subject': subject, \
        'text_messege': text_messege}

    return item

client = MongoClient('localhost', 27017)
mybase = client['mail_db']
mycoll = mybase['messages']

driver = webdriver.Chrome('c:\chromedriver.exe')

driver.get('https://yandex.ru/')

assert 'Яндекс' in driver.title

try:
    mail_button = driver.find_element_by_css_selector(
        'div.desk-notif-card__login-new-items a'
    )

    mail_button.click()

    driver.title

    if 'Авторизация' in driver.title:
        login_form = driver.find_element_by_css_selector('div[class="passp-auth"]')

        field_login = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'passp-field-login')))
        field_login.send_keys('stanka78')
        field_login.send_keys(Keys.ENTER)
        field_passwd = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'passp-field-passwd')))
        field_passwd.send_keys('123456789#')
        field_passwd.send_keys(Keys.ENTER)
        mail_enter = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'desk-notif-card__domik-mail-line')))
        mail_enter.click()

        driver.switch_to_window (driver.window_handles[1])

        first_messege = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'ns-view-messages-item-wrap')))
        first_messege.click()

        while True:
            try:

                time.sleep(10)

                mycoll.insert_one(parse_email(driver))

                time.sleep(10)

                button_next = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'PrevNext__link--1RPpF')))

                time.sleep(10)
                button_next.click()

            except exceptions.ElementClickInterceptedException:
                print('Cannot Click Next Button')
                break

            except exceptions.TimeoutException:
                print('E-mails are over')
                break

except exceptions.NoSuchElementException:
    print('Mail login not found')

driver.quit()
