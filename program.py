import csv

from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

Driver_path="C:/Selenium/geckodriver.exe"

def get_html(url):
    # This function is used to open the links passed through the csv file.
    driver=webdriver.Firefox(executable_path=Driver_path)
    driver.get(url)
    driver.implicitly_wait(10)
    data=driver.page_source
    # driver.close()
    return data
def scrape(url):

   # This function will be called by webdriver when the page is loaded for the scraping
    html=get_html(url)
    Soup = BeautifulSoup(html, "lxml")

    try:
        Title=Soup.find(id = "productTitle").get_text().strip()

        try:
            Price=Soup.select_one("#olp_feature_div .a-color-price").text
        except:
            Price=Soup.select_one("span.a-color-base span").text

        try:
            Desc=Soup.select_one("#feature-bullets .a-list-item").text.strip()
        except:
            Desc=Soup.select_one("div.a-expander-content span").text

        try:
            # image location for products
            img=Soup.select_one("#imgTagWrapperId img[src]")['src']
        except:
            # image link for books as it is at different location
            img=Soup.select_one('#img-canvas img[src]')['src']

        my_dict={'Product Title':Title,'Product Image URL':img,'Price of the Product':Price,'Product Details':Desc}

        return my_dict

    except:
        print(f'{url} is not available')
        return None
def start():
    df = pd.read_csv("C:/Users/Acer/Downloads/data.csv") # This will load the file i had it saved on my local disk
    results=[]
    for i in range(100):
        Asin=df['Asin'][i]
        Country=df['country'][i]
        url=f'https://www.amazon.{Country}/dp/{Asin}'

        # if requests.get(url).status_code!=404 and requests.get(url).status_code!=503:
        #     print(requests.get(url).status_code)
        data=scrape(url)
        if data is not None:
            results.append(data)
    write_csv(results)

def write_csv(data):
    with open("results.csv",'a',encoding='utf-8') as f:
        fields=['Product Title','Product Image URL','Price of the Product','Product Details']
        writer=csv.DictWriter(f,fieldnames=fields)
        for m in data:
            writer.writerow(m)
start() # Here the main function is called
