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

driver.get("https://www.google.com")
driver.quit()

urls=get_url("logos.csv")
print(urls)