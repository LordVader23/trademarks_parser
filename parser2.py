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


class Bot2(Bot):
    FILE_NAME = 'trademarks2.csv'

    def __init__(self):
        super().__init__()

    def run(self):
        wait2 = WebDriverWait(self.driver, 15)

        self.driver.get('https://www3.wipo.int/branddb/en/index.jsp#')

        self.wait_loader()

        country_button = self.driver.find_element_by_css_selector("a['href'='#country_search']")
        country_button.click()

        designation_input = self.driver.find_element_by_css_selector("input#DS_input")
        designation_input.send_keys('KZ')

        search_button = self.driver.find_element_by_css_selector(
                                                        "div.searchButtonContainer.bottom.right a span.ui-button-text")
        search_button.click()

    def get_trademarks(self):
        pass

    def wait_loader(self):
        while True:
            sleep(3)

            try:
                loader = self.driver.find_element_by_css_selector("div.pagerAjaxIcon.ajaxIcon")
            except NoSuchElementException:
                break


if __name__ == '__main__':
    b = Bot2()
    b.run()
