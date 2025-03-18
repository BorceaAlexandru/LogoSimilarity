import requests
import os
import pandas as pd

def add_protocol(url):
    if not url.startswith(("http://", "https://")):
        return f"https://{url}"
    return url

def access_verification(url):
    try:
        response = requests.get(url, timeout=30)
        return response.status_code == 200
    except Exception as e:
        print(f"Website {url} is not accessible: {e}")
        return False

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
