from time import sleep
import time
import click
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common import actions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from webdriver_manager.firefox import GeckoDriverManager


url1= "https://karararama.yargitay.gov.tr/YargitayBilgiBankasiIstemciWeb/"

driver2 = webdriver.Firefox(
         service=Service(
            GeckoDriverManager().install()
         )
)

driver2.get(url1)
driver2.find_elements(By.ID, "ali")

logo_we = WebDriverWait(driver2, 10).until(
   EC.presence_of_element_located(
      (By.CSS_SELECTOR, "img[class='img-responsive logo']")
   )
)
#logo_we = driver2.find("img-responsive logo")
print(logo_we)
print(logo_we.location)

detayli_arama_we = WebDriverWait(driver2, 10).until(
         EC.presence_of_element_located(
            (By.ID, "aramaForm:detayliAramaLabel")
         ))

detayli_arama_we.click()

ara = WebDriverWait(driver2, 10).until(
   EC.presence_of_element_located(
      (By.CSS_SELECTOR, "span[class='ui-button-text ui-c']")
   )
)


#print("BURA" + ara.get_attribute('innerHTML'))
#print(logo_we.location_once_scrolled_into_view)

time.sleep(5)