import asyncio
import json
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
from queue import Queue
import random
import traceback
from datetime import datetime as dt, timedelta


class LinkMonitor:
    def __init__(self, queue):
        self.queue = queue
        self.config = json.load(open('config.json'))
        self.vm_url = 'http://selenium:4444/wd/hub'
        self.base_url = 'https://s2.coinmarketcap.com/static/img/coins/64x64'
        self.number = self.config.get('STARTING_CHECK_IMAGE_NUMBER')
        self.dc = DesiredCapabilities.CHROME
        self.next_time = dt.now() + timedelta(hours=4)

    def get_url(self):
        return f'{self.base_url}/{self.number}.png'

    def start(self):
        self.chrome_options = webdriver.ChromeOptions()
        # self.chrome_options.add_argument('--headless')
        self.driver = webdriver.Remote(
            self.vm_url, desired_capabilities=self.dc)
        # self.driver.implicitly_wait(5)
        self.loop = asyncio.new_event_loop()
        self.loop.run_until_complete(self.main())

    async def main(self):
        while True:
            URL = self.get_url()
            image = await self.get_image(URL)
            if not image:
                current = dt.now()
                if current >= self.next_time:
                    # Timeout waiting for image ..
                    self.number += 1
                    URL = self.get_url()
                    image = await self.get_image(URL)
                    if image:
                        search_url = await self.create_google_image_search(URL)
                        self.queue.put((image, search_url))
                        self.number += 1
                        self.next_time = dt.now() + timedelta(hours=4)
                        continue
                    self.number -= 1

                continue
            print(f'Image found on {URL}')
            # await self.random_sleep(2, 3)
            search_url = await self.create_google_image_search(URL)
            self.number += 1
            self.queue.put((image, search_url))
            # await asyncio.sleep(2)

    async def get_image(self, URL):
        try:
            self.driver.get(URL)
            soup = BeautifulSoup(self.driver.page_source, features="lxml")
            img = soup.find("img")
            return img.get_attribute_list("src")[0] if img else None
        except Exception as e:
            traceback.print_exc()
            return None

    async def create_google_image_search(self, image_url):
        print('Creating google image search URL ...')
        try:
            self.driver.get("https://images.google.com")
            # await self.random_sleep(1, 2)
            upload = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/form/div[1]/div[1]/div[1]/div/div[3]/div[2]")
            upload.click()
            # await self.random_sleep(2, 5)
            box = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div/div[2]/form/div[1]/table/tbody/tr/td[1]/input")
            box.send_keys(image_url)
            # await self.random_sleep(2, 5)
            search_btn = self.driver.find_element_by_xpath(
                "/html/body/div[2]/div[2]/div/div/div[2]/form/div[1]/table/tbody/tr/td[2]/input")
            search_btn.click()
            # await self.random_sleep(1, 3)
            return self.driver.current_url
        except Exception as e:
            traceback.print_exc()

    async def random_sleep(self, a, b):
        await asyncio.sleep(random.randint(a, b))


if __name__ == '__main__':
    monitor = LinkMonitor(Queue())
    monitor.start()
