import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import requests


#config gecko
service=Service("geckodriver.exe")
options = Options()
options.headless=True #rulare in fundal fara interfata grafica
options.accept_insecure_certs=True #invalid ssl certificates
options.set_preference("general.useragent.override",
                       "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
driver=webdriver.Firefox(service=service,options=options)
driver.set_page_load_timeout(30) #timeout set to 30secs

#adding protocol to each website
def add_protocol(url):
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url

#get urls from csv file
def get_url(csv):
    if not os.path.exists(csv):
        print("File not found!")
        return []
    try:
        df=pd.read_csv(csv)
        if df.empty:
            print("Empty file!")
            return []

        urls=df[df.columns[0]].dropna()
        print("URL extraction works!")
        return urls.tolist()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []


#website access verification
def access_verification(url):
    try:
        response = requests.get(url, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"Website {url} is not accessible: {e}")
        return False


#get logooos
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

#main
def main():
    urls=get_url("logos.csv")
    if not urls:
        print("No URLs found!")
        return

    #all websites should have protocol
    urls=[add_protocol(url) for url in urls]

    if os.path.exists("logos_urls.json"):
        with open("logos_urls.json", "r") as f:
            try:
                logo_urls=json.load(f)
            except json.JSONDecodeError:
                logo_urls={}
    else:
        logo_urls={}

    for url in urls:
        print("Processing URL:", url)
        if access_verification(url):
            logo_url=get_logo(driver, url)
            if logo_url:
                logo_urls[url]=logo_url

                with open("logos_urls.json", "w") as f:
                    json.dump(logo_urls, f, indent=4)
                print(f"Saved logo URL for {url}")
        else:
            print(f"Skipping {url} because it is not accessible!")

    driver.quit()
    print("Done!")

if __name__=="__main__":
    main()