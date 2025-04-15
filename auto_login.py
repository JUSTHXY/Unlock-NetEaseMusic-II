# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "0031D58F1B0A095DCB918940AB1818ABD7440BE195EFF5786270D0452611CACE7B646E80A0F8182948A88971DA2B46DED34F5B1A6B2E0E7E7C5EEEA5E8666A0126CB7FEBF1A47181ED4CA851932C697368029EEE433F2C48F4EA9274218359766A00D236CA3BAF8FB5D866CA785388F74A2DDC4EAC7673E437C07B7542DB122D5C8A8F81D6608AD4DC7086139303DD8CF8DB5B237B2FEAEBF630782DBDFA438ED9E33BE4E8ABFF3824D0141AF607BE62F70AD0BB8DCE1B938D749052E9C4A33C88B1D86E2F1A3BCC4A32DABE44F1BE0E137F4E0F4F76E9FC8C62BFEEE293664E36528C15724BE5FD0540EC305A6ED399066007DE02B4E9442B87689D35C30272A840BC5237691238A2C53F0A9B2C8538702A20F1C7BA4C4047DBE414057819424EEFF242A4C3E4119611DC910729969469990B340EDDF6E9F7833BE65F1C59C535E7AC38FEBDE31F2A7F2B3434F951BE34"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
