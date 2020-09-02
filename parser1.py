from selenium import webdriver
from time import sleep
from PIL import Image


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

        print(data)

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
