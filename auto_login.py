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
    browser.add_cookie({"name": "MUSIC_U", "value": "00233C0BE9AF3C03CFBF946D7B90C7B18DC0E150BA4EE075FD860184F4868B1C92BAC6F7907A9FD484D42B678B57F1750EC687CE3FEE3BD4E90F1B51A83C2D1B85E8634E9B36D408435B306BC91EF785A74B3A2C698B51F0CD5C6AEB945457E691D7D13A2E9425BB0AB829F7E5675C84778899493A040188C3669E79EC8176E4D8122D96AC37D9C2638CB08227EA463BB83968F6C06723694FB36EA23A5046B7222D68AD09EA23C1AC5924257593DA124C1D54F464547BFEDF669D0F254E45D69EC76215AA7BBC6EB29A712EEF562625E0CD7760603A585C8E908E405CE457214DDAC334F8AE022BE5216CE40FD0D9D91AE0C39ECDA86F2FED2F790DAC4F8C3AB776CB10E1D73261EAE523FBC570CF75F0173C3A07984873EA2AF4D8C49D963C3D7B7C9E117AD8CE4B43FDE6D7AEC51D03BF98843E649ED71EF6FA9119E85B6D5D93BAF181A1595BD2E9A79AF7FAD07C7D1F76239594940F84766D2042AC92768B"})
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
