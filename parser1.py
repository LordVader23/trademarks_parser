from selenium import webdriver
from time import sleep
from PIL import Image
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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

    def get_trademarks(self):
        # Wait before element is clickable
        wait2 = WebDriverWait(self.driver, 10)
        wait2.until(EC.staleness_of(self.driver.find_elements_by_css_selector("td.dxflNestedControlCell_Material")[0]))

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

        while info:
            a1 = info[0:9]
            a1.append(img_links[0])
            data.append(a1)

            del info[0:9]
            del img_links[0]

        try:
            next_page_button = self.driver.find_element_by_css_selector("b.dxp-button.dxp-bi.dxp-disabledButton")
        except Exception:
            return None
        else:
            next_page_button = self.driver.find_element_by_css_selector("img.dxWeb_pNext_Material")
            next_page_button.click()

        return self.get_trademarks()

    def write_csv(self, data):
        data_row = [
            data['title'],
            data['price'],
        ]

        with open('coin_market.csv', 'a+', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(data_row)


if __name__ == '__main__':
    b = Bot()
    b.run()
