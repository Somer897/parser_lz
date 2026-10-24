#Вариант 2  ---  AMD
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import random
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
import unicodedata
import pandas as pd

def logging(func):
    log_data = {
        "Function": [func],
        "Time": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        "User": [os.environ.get('USERNAME')],
    }
    df = pd.DataFrame(log_data)
    df.to_csv('logging.csv', index=False, mode="a", sep=";", header=not os.path.isfile('logging.csv'), encoding="utf-8-sig"
    )

class Parser:

    def __init__(self, link):
        self.link = link
        self.pilesosi = []
        self.date_dict = {}
        options = ChromeOptions()
        options.add_argument(f"--proxy-server=http://159.195.53.110:3128")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument(f"--user-agent=USER_AGENT = ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
        options.page_load_strategy = 'normal' 
        self.driver = webdriver.Chrome(options=options)

    def search(self):
        self.driver.get(self.link)

        cookies = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[19]/div/div/div[3]/button")))
        self.driver.execute_script("arguments[0].click();", cookies)

        filter1 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "ocf-v-40866-1-739373-1")))
        self.driver.execute_script("arguments[0].click();", filter1)

        filter2 = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, "ocf-v-40866-1-664764-1")))
        self.driver.execute_script("arguments[0].click();", filter2)

        use_filters = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "ocf-search-btn-static")))
        self.driver.execute_script("arguments[0].click();", use_filters)

        div = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[5]')
        cards = div.find_elements(By.CLASS_NAME, value='title')
        links = []
        for card in cards:
            links.append(card.find_element(By.TAG_NAME, 'a').get_attribute('href'))

        self.pilesosi = links

    def get_tables(self):
        for link in self.pilesosi:
            self.driver.get(link)
            time.sleep(random.uniform(4.5, 5.5))
            table = self.driver.find_element(By.ID, value='tab-1')
            chars = table.find_elements(By.CLASS_NAME, value='specs__row')
            name = self.driver.find_element(By.CLASS_NAME, value='specs__product')
            self.date_dict.update({'Название' : name.get_attribute("textContent")})

            for char in chars:
                left = char.find_element(By.CLASS_NAME, value='specs__name-text')
                text_1 = left.get_attribute("textContent")
                right = char.find_element(By.CLASS_NAME, value='specs__value')
                text_2 = right.get_attribute("textContent")
                text_2 = unicodedata.normalize("NFKD", text_2)
                self.date_dict.update({text_1 : [text_2]})

    
            df_1 = pd.DataFrame(self.date_dict)
            df_1.to_csv("var.csv", index=False,  mode="a", sep=",", header=not os.path.isfile("var.csv"), encoding='utf-8-sig')



def main():
    parser = Parser('https://www.amd.by/roboty-pylesosy/')
    logging('__init__')
    parser.search()
    logging('search')
    parser.get_tables()
    logging('get_tables')

if __name__ == '__main__':
    main()