import time
from selenium import webdriver
import os
dir_path = os.path.realpath(os.getcwd())


from module import Module

class inspiro(Module):

    async def get_inspiro(self):
        ENV = os.getenv('ENVIRONMENT')
        driver = 0
        if ENV == "windows":
            path = '\\'.join(dir_path.split("\\")) + "\lib\chromedriver.exe"
            driver = webdriver.Chrome(executable_path=path)
        else:
            options = webdriver.ChromeOptions() 
            options.add_argument("--headless")
            options.add_argument("--disable-dev-shm-usage")
            options.addArguments("--no-sandbox")
            driver = webdriver.Chrome(chrome_options=options)
        driver.get("https://inspirobot.me/")
        button = driver.find_element_by_class_name("button-wrapper")
        button.click()
        time.sleep(5)
        image = driver.find_element_by_class_name("generated-image")
        url = image.get_attribute("src")
        driver.quit()
        await self.reply(url)
