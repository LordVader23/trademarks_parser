from selenium import webdriver
from time import sleep
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import csv


class Bot:
    def __init__(self):
        self.driver = webdriver.Firefox(executable_path="/home/lordvader/Загрузки/geckodriver")

    def run(self):
        self.driver.get('http://gosreestr.kazpatent.kz/')

        register = self.driver.find_element_by_css_selector("td[id='cbReestrType_B-1']")
        register.click()

        trademarks = self.driver.find_element_by_css_selector("td[id='cbReestrType_DDD_L_LBI5T0']")
        trademarks.click()

        findButton = self.driver.find_element_by_css_selector("button[id='btnSearch']")
        findButton.click()

        sleep(5)

        self.get_trademarks()

    def wait_more(self, wait_obj, ec):
        while True:
            try:
                wait_obj.until(ec)
            except TimeoutException:
                self.wait_more(wait_obj, ec)
            else:
                break

    def get_trademarks(self):
        wait2 = WebDriverWait(self.driver, 15)

        # try:
        #     ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
        #     all_info = WebDriverWait(self.driver, 10, ignored_exceptions=ignored_exceptions).until(
        #         EC.presence_of_element_located((By.CSS_SELECTOR, 'td.dxflNestedControlCell_Material')))
        # except :
        #     self.get_trademarks()

        # while True:
        #     try:
        #         wait2.until(EC.element_to_be_clickable((By.CSS_SELECTOR,
        #                                             "td.dxflNestedControlCell_Material")))
        #     except TimeoutException:
        #         self.wait_more()
        #     else:
        #         break

        # To wait
        self.wait_more(wait2, EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    "td.dxflNestedControlCell_Material")))
        # wait2.until(
        #     EC.staleness_of(self.driver.find_elements_by_css_selector("span[id='cvContracts_DXCardLayout0_0_Cap']")[0]))

        all_info = self.driver.find_elements_by_css_selector("td.dxflNestedControlCell_Material")
        info = []

        images = self.driver.find_elements_by_css_selector("img.dxeImage_Material")
        img_links = []

        # Get img links
        for img in images:
            link = img.get_attribute('src')
            img_links.append(link)

        # To extract elem text
        for elem in all_info:
            info.append(elem.text)

        data = []

        # To generate data
        while info:
            a1 = info[0:9]
            a1.append(img_links[0])
            data.append(a1)

            del info[0:9]
            del img_links[0]

        self.write_csv(data)
        # To paginate
        try:
            # sleep(9)
            # next_page_button = self.driver.find_element_by_css_selector("b.dxp-button.dxp-bi.dxp-disabledButton")
            self.wait_more(wait2, EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                    "img.dxWeb_pNext_Material")))

            next_page_button = self.driver.find_element_by_css_selector("img.dxWeb_pNext_Material")
            next_page_button.click()
        except Exception:
            return None

        self.get_trademarks()

    def write_csv(self, data):
        with open('trademarks1.csv', 'a+', encoding='utf-8') as f:
            writer = csv.writer(f)

            for data_row in data:
                writer.writerow(data_row)


if __name__ == '__main__':
    b = Bot()
    b.run()
