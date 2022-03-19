
import time
from Driver import Driver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait



x=[0]
url1= "https://karararama.yargitay.gov.tr/YargitayBilgiBankasiIstemciWeb/"

driver1 = Driver(url1, x)
driver1.connect_driver()

driver1.get_detayli_arama_we().click()

driver1.get_karar_yili_we().send_keys("2021")

driver1.get_radio_button_karar_we()[0].click()


driver1.get_son_karar_no_input_we().location_once_scrolled_into_view

WebDriverWait(driver1.driver, 10).until(
   EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input[id='aramaForm:ilkKararNoInput']")
   )
)

driver1.get_ilk_karar_no_input_we().send_keys("123")
driver1.get_ilk_esas_no_input_we().location_once_scrolled_into_view

driver1.get_radio_button_karar_we()[1].click()

time.sleep(3)


WebDriverWait(driver1.driver, 10).until(
   EC.element_to_be_clickable(
      (By.CSS_SELECTOR, "input[id='aramaForm:sonKararNoInput']")
   )
).send_keys("200")

time.sleep(1000)


