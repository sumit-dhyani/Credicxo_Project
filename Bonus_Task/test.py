import os
from selenium import webdriver
from selenium.webdriver.common.by import By

from google.cloud import vision
credential_path = "C:/Users/Acer/New_Folder/coastal-epigram-345703-2e7c24676f7a.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def webpage(url):
    driver=webdriver.Chrome(executable_path="C:/Selenium/chromedriver.exe")
    driver.implicitly_wait(10)
    driver.get(url)
    urls=driver.find_element(By.CSS_SELECTOR,"body > div > div.a-row.a-spacing-double-large > div.a-section > div > div > form > div.a-row.a-spacing-large > div > div > div.a-row.a-text-center > img").get_attribute('src')
    text=detect_text_uri(urls)
    inputbox=driver.find_element(By.ID,"captchacharacters")
    inputbox.send_keys(text)
    driver.find_element(By.CLASS_NAME,"a-button-text").click()
    
def detect_text_uri(uri):
    # it will request text recognization for the image sent to google vision api
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.text_detection(image=image)
    texts = response.text_annotations
    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    return texts[0].description.strip()

webpage("https://www.amazon.com/errors/validateCaptcha")