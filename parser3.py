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


class Bot3(Bot):
    FILE_NAME = 'trademarks3.csv'

    def __init__(self):
        super().__init__()
        self.driver.set_window_size(1024, 720)

    def run(self):
        wait2 = WebDriverWait(self.driver, 15)

        self.driver.get('https://www3.wipo.int/branddb/en/index.jsp#')

        self.wait_loader()

        country_button = self.driver.find_element_by_css_selector("a[href='#country_search']")
        country_button.click()

        designation_input = self.driver.find_element_by_css_selector("input#DS_input")
        designation_input.send_keys('KZ')

        sleep(3)
        ul = self.driver.find_element_by_css_selector("ul#ui-id-26")
        ul.click()

        # some_div = self.driver.find_element_by_css_selector("div.desc")
        # some_div.click()

        sleep(5)
        search_button = self.driver.find_element_by_css_selector(
                                                        "div.searchButtonContainer.bottom.right a span.ui-button-text")
        # search_button.click()
        self.driver.execute_script("arguments[0].click();", search_button)

        self.get_trademarks()

    def get_trademarks(self):
        self.wait_loader()  # To wait until page is loaded
        sleep(3)

        brands = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_BRAND']")
        sources = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_SOURCE']")
        statuses = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_STATUS']")
        relevans = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_score']")
        origins = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_OO']")
        holders = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_HOL']")
        holder_countries = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_HOLC']")
        nums = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_ID']")
        app_dates = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_AD']")
        img_classes = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_LOGO']")
        nices = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_NC']")
        imgs = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_IMG']")
        links = self.driver.find_elements_by_css_selector("td[aria-describedby='gridForsearch_pane_IMG'] img")

        arr = zip(brands, sources, statuses, relevans, origins, holders, holder_countries,
                  nums, app_dates, img_classes, nices, imgs)
        data = []

        for elem in arr:
            data_row = []

            for i in elem[:-1]:
                if i.text == ' ':
                    data_row.append('')
                else:
                    data_row.append(i.text)

            if elem[-1].text == ' ':
                data_row.append('')
            else:
                data_row.append(links[0].get_attribute('src'))
                del links[0]

            data.append(data_row)

        self.write_csv(data)
        # To paginate
        try:
            # self.wait_more(wait2, EC.element_to_be_clickable((By.CSS_SELECTOR,
            #                                                   "a[aria-label='next page']")[0]))

            next_page_button = self.driver.find_elements_by_css_selector(
            "a.toolTip.ui-button.ui-widget.ui-state-default.ui-corner-all.ui-button-icon-only span.ui-button-icon-primary.ui-icon.ui-icon-triangle-1-e")
            next_page_button[0].click()
        except Exception:
            return None

        self.get_trademarks()

    def wait_loader(self):
        while True:
            sleep(3)

            try:
                loader = self.driver.find_element_by_css_selector(
                    "div.results_navigation.top_results_navigation.displayButtons.hover div.pagerAjaxIcon.ajaxIcon")
            except NoSuchElementException:
                break


if __name__ == '__main__':
    b = Bot3()
    b.run()
