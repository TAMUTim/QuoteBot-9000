from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

import os
import time
import json


def post_handler(event, context):
    # LINKEDIN_SITE = 'https://www.linkedin.com'
    LINKEDIN_SITE = os.environ.get("LINKEDIN_SITE")
    LINKEDIN_USER = os.environ.get("LINKEDIN_USER")
    LINKEDIN_PASS = os.environ.get("LINKEDIN_PASS")

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(LINKEDIN_SITE)
    time.sleep(5)

    try:
        driver.find_element(By.XPATH, '//*[@id="session_key"]').send_keys(LINKEDIN_USER)
        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="session_password"]').send_keys(LINKEDIN_PASS)
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, 'sign-in-form__submit-btn--full-width').click()
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, 'share-box-feed-entry__trigger').click()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, 'ql-editor.ql-blank').send_keys(event['content'])
        time.sleep(5)
        driver.find_element(By.CLASS_NAME, 'share-actions__primary-action').click()
        time.sleep(5)

        body = {
            "message": "Successfully uploaded!"
        }
        return {"statusCode": 200, "body": json.dumps(body)}
    except NoSuchElementException as err:
        return {"statusCode": 500, "body": json.dumps({"message": "Issue finding an element, please try again"})}
    except ElementClickInterceptedException as err:
        return {"statusCode": 501, "body": json.dumps({"message": "Click was intercepted, contact Tim for further diagnoses"})}
    