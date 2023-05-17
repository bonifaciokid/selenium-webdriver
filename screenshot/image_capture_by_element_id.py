"""
- Screen capture specific element
- Image will be used for og:image
- "screenshot_as_png" can only be used on Python3.8 version and above
"""
import json
import time
import boto3
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

import sys
sys.path.insert(1, "/var/scrapy/functions")
import db_connections

with open("/var/jsonfiles/scrapy-configs.json", "r") as aws:
    AWS_CONFIG = json.load(aws)

S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=AWS_CONFIG["aws_keys"]["access_key"],
    aws_secret_access_key=AWS_CONFIG["aws_keys"]["secret_key"]
)

USER_AGENT = 'user-agent'
OPTIONS = Options()
OPTIONS.add_argument("--headless") # headless browser
OPTIONS.add_argument("--window-size=1920,1080") # set window size
OPTIONS.add_argument("--no-sandbox")
OPTIONS.add_argument(f"--user-agent={USER_AGENT}")
PATH = "/path/to/chromedriver"
SERVICE = Service(PATH)
DRIVER = webdriver.Chrome(service=SERVICE, options=OPTIONS)


def put_image_to_s3_bucket(image_buffer, item_id):
    """
    - save image to s3 bucket
    - Args
        - image_buffer
            - image
        - page
    """
    print("save image to s3 bucket...")
    object_key = f"{item_id}.jpg"
    S3_CLIENT.put_object(
        Bucket='wtp-og-images',
        Key=object_key,
        Body=image_buffer.getvalue(),
        CacheControl='public, max-age=31536000',
        ContentType=f'image/jpg'
    )
    return True


def screenshot_og_image(items):
    """
    - Capture specific element
    - Arg
        - items
            - In this example items are list of list ex.
              [[url, item_id_1], [url, item_id_2]]...
            - url
                - url string
                - will be the webpage
            - item_id
                - integer
                - will be used to name captured image
    """
    if items:
        for url, item_id in items:
            print(f"open web {url}...")
            DRIVER.get(url)
            time.sleep(15)
            try:
                print('find id "screencap"...')
                element = DRIVER.find_element(By.ID, 'screencap')
            except NoSuchElementException:
                element = None

            if element:
                # set padding to 50 px
                padding_value = "50px"
                DRIVER.execute_script(f"arguments[0].style.padding = '{padding_value}'", element)
                time.sleep(5)

                # capture image
                screencap_element = DRIVER.find_element(By.ID, 'screencap')
                screenshot = screencap_element.screenshot_as_png
                image_buffer = BytesIO(screenshot)

                # save image
                put_image_to_s3_bucket(image_buffer, item_id)
            else:
                print('cannot find id, "screencap"...')
    else:
        print(f'no new items...end')


def main():
    items = [["https://sample.com/", "item_1"]]
    screenshot_og_image(items)


if __name__ == "__main__":
    main()
