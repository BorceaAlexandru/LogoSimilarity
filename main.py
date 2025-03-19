import os
import json
from config.settings import GECKODRIVER_PATH, FIREFOX_OPTIONS, PAGE_LOAD_TIMEOUT
from services.logo_processor import download_logo, process_image
from utils.helpers import add_protocol, access_verification, get_url
from services.web_scraper import init_driver, get_logo
from services.extractor import extract
from services.clustering import group_logos
from utils.output_helpers import save_grouped_logos

def main():

    #get urls from csv
    urls=get_url("data/logos.csv")
    if not urls:
        print("No URLs found!")
        return

    #add protocol if needed
    urls=[add_protocol(url) for url in urls]

    #get logos urls
    if os.path.exists("outputs/logos_urls.json"):
        with open("outputs/logos_urls.json", "r") as f:
            try:
                logo_urls=json.load(f)
            except json.JSONDecodeError:
                logo_urls={}
    else:
        logo_urls={}

    #selenium setup
    driver=init_driver()
    descriptors_list=[]     #orb descriptors
    valid_urls=[]           #valid urls

    try:
        #extract logo from each url
        for i, url in enumerate(urls):
            print("Processing URL: ", url)
            if access_verification(url):
                logo_url=get_logo(driver, url)
                if logo_url:
                    logo_urls[url]=logo_url

                    #download and process image
                    save_path=f"outputs/logo_{i}.png"
                    download_logo(logo_url, save_path)
                    process_image(save_path)

                    #extract
                    keypoints, descriptors=extract(save_path)
                    if descriptors is not None:
                        descriptors_list.append(descriptors)
                        valid_urls.append(url)
                        print(f"Extracted {len(descriptors)} features from {save_path}")

                    #write in json file
                    with open("outputs/logos_urls.json", "w") as f:
                        json.dump(logo_urls, f, indent=4)
                    print(f"Saved logo URL for {url}")
            else:
                print(f"Skipping {url} because is not accessible!")
    finally:
        driver.quit()
        print("Browser closed!")

    #group logos based on similarity
    if descriptors_list:
        labels=group_logos(descriptors_list)
        save_grouped_logos(valid_urls, labels, "outputs/group_logos.json")
    else:
        print("No descriptors found for clustering!")

    print("Done!")

if __name__ == "__main__":
    main()