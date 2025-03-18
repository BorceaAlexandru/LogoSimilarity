import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json


#config gecko
service=Service("geckodriver.exe")
options = Options()
options.headless=True #rulare in fundal fara interfata grafica
driver=webdriver.Firefox(service=service,options=options)

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


#get logooos
def get_logo(driver, url):
    try:
        driver.get(url)
        #added timeout
        logo_element=WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//img[contains(@class, "logo")]'))
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

    logo_urls={}
    for url in urls:
        print("Processing URL:", url)
        logo_url=get_logo(driver, url)
        if logo_url:
            logo_urls[url]=logo_url

    driver.quit()

    #save data in json file
    with open("logo_urls.json","w") as f:
        json.dump(logo_urls,f, indent=4)
    print("Done!")

if __name__=="__main__":
    main()