import os
import json
import pandas as pd
from config.settings import GECKODRIVER_PATH, FIREFOX_OPTIONS, PAGE_LOAD_TIMEOUT
from utils.helpers import add_protocol, access_verification, get_url
from services.web_scraper import init_driver, get_logo

def main():
    urls=get_url("data/logos.csv")
    if not urls:
        print("No URLs found!")
        return

    urls=[add_protocol(url) for url in urls]

    if os.path.exists("outputs/logos_urls.json"):
        with open("outputs/logos_urls.json", "r") as f:
            try:
                logo_urls=json.load(f)
            except json.JSONDecodeError:
                logo_urls={}
    else:
        logo_urls={}

    driver=init_driver()
    try:
        for url in urls:
            print("Processing URL: ", url)
            if access_verification(url):
                logo_url=get_logo(driver, url)
                if logo_url:
                    logo_urls[url]=logo_url
                    with open("outputs/logos_urls.json", "w") as f:
                        json.dump(logo_urls, f, indent=4)
                    print(f"Saved logo URL for {url}")
            else:
                print(f"Skipping {url} because is not accessible!")
    finally:
        driver.quit()
        print("Browser closed!")
    print("Done!")

if __name__ == "__main__":
    main()