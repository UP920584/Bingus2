import time
from selenium import webdriver
import os
dir_path = os.path.realpath(os.getcwd())


from module import Module

class inspiro(Module):

    async def get_inspiro(self):
        PATH = os.getenv('ENVIRONMENT')

        options = webdriver.ChromeOptions() 
        options.add_argument("--headless") # prevents chromedriver opening a window
        options.add_argument("--disable-dev-shm-usage") # prevents chromedriver from using space where we wouldnt have any
        options.add_argument("--no-sandbox") # temporaray fix

        driver = webdriver.Chrome(PATH, chrome_options=options)
        driver.get("https://inspirobot.me/")
        button = driver.find_element_by_class_name("button-wrapper")
        driver.execute_script('window.scrollTo(0, ' + str(button.location['y']) + ');')
        button.click()
        time.sleep(5)
        image = driver.find_element_by_class_name("generated-image")
        url = image.get_attribute("src")
        driver.quit()
        await self.reply(url)
