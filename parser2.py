from selenium import webdriver
from time import sleep
from PIL import Image
from parser1 import Bot
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import csv
import datetime
import re


class Bot2(Bot):
    FILE_NAME = 'trademarks2.csv'

    def __init__(self):
        super().__init__()

    def run(self):
        wait2 = WebDriverWait(self.driver, 15)

        self.driver.get('https://ebulletin.kazpatent.kz/patents/1276/4/1')

        self.wait_more(wait2, EC.element_to_be_clickable((By.CSS_SELECTOR,
                        "td.mat-cell.cdk-column-applicationNumber.mat-column-applicationNumber.ng-star-inserted")))

        self.get_trademarks()

    def get_trademarks(self):
        wait2 = WebDriverWait(self.driver, 15)

        self.wait_loader()
        self.wait_more(wait2, EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                          "td.mat-cell.cdk-column-applicationNumber.mat-column-applicationNumber.ng-star-inserted")))
        sleep(3)

        numbers = self.driver.find_elements_by_css_selector(
            "td.mat-cell.cdk-column-applicationNumber.mat-column-applicationNumber.ng-star-inserted")
        dates = self.driver.find_elements_by_css_selector(
            "td.mat-cell.cdk-column-applicationDate.mat-column-applicationDate.ng-star-inserted")
        owners = self.driver.find_elements_by_css_selector(
            "td.mat-cell.cdk-column-owner.mat-column-owner.ng-star-inserted")
        images = self.driver.find_elements_by_css_selector(
            "td.mat-cell.cdk-column-image.mat-column-image.ng-star-inserted img")
        codes = self.driver.find_elements_by_css_selector(
            "td.mat-cell.cdk-column-icgsCode.mat-column-icgsCode.ng-star-inserted")

        arr = zip(numbers, dates, owners, codes, images)

        data = []

        for elem in arr:
            data_row = []

            date = datetime.datetime.strptime(elem[1].text, "%d.%m.%Y")
            date_now = datetime.datetime.today()

            if (date_now - date).days >= 8 * 30:
                continue

            for i in elem[:-1]:
                data_row.append(i.text)

            data_row.append(elem[-1].get_attribute('src'))

            data.append(data_row)

        self.write_csv(data)
        # To paginate
        if self.check_if_last_page():
            return None
        else:
            next_page_button = self.driver.find_elements_by_css_selector("svg.mat-paginator-icon")
            next_page_button[1].click()
            self.get_trademarks()

    def wait_loader(self):
        while True:
            sleep(3)

            try:
                loader = self.driver.find_element_by_css_selector("div.cube-loader.ng-star-inserted")
            except NoSuchElementException:
                break

    def check_if_last_page(self):
        """
        Checks if page is last
        :return: True or False
        """
        page_number = self.driver.find_element_by_css_selector("div.mat-paginator-range-label").text
        match = re.search(r'([0-9]+) of ([0-9]+)', page_number)

        if match[1] == match[2]:
            return True
        else:
            return False


if __name__ == '__main__':
    b = Bot2()
    b.run()
