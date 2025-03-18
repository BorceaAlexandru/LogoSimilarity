from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.settings import GECKODRIVER_PATH, FIREFOX_OPTIONS, PAGE_LOAD_TIMEOUT

def init_driver():
    service=Service(GECKODRIVER_PATH)
    options = Options()
    for key, value in FIREFOX_OPTIONS.items():
        options.set_preference(key, value)
    driver=webdriver.Firefox(service=service, options=options)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver

def get_logo(driver, url):
    try:
        driver.get(url)
        #added timeout
        logo_element=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//img[contains(@class, "logo") or contains(@id, "logo") or contains(@alt, "logo")]'))
        )
        logo_url=logo_element.get_attribute("src")
        return logo_url
    except Exception as e:
        print(f"Error getting logo from {url}: {e}")
        return None
