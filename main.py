import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

#config gecko
service=Service("geckodriver.exe")
options = Options()
options.headless=True #rulare in fundal fara interfata grafica

driver = webdriver.Firefox(service=service,options=options)

#scot url din fisier
def get_url(csv):
    if os.path.exists(csv):
        df=pd.read_csv(csv)
        print("URL extraction works!")
    else:
        print("File not found!")
        return []

    urls=df[df.columns[0]].dropna()
    return urls.tolist()

driver.get("https://www.google.com")
driver.quit()

urls=get_url("logos.csv")
print(urls)