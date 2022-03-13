from selenium.webdriver.common.keys import Keys
import captcha
import time
from selenium.webdriver.common.action_chains import ActionChains
from my_tools import get_str_date


from Driver import Driver

def download_data(start_date, end_date):

   url1= "https://karararama.yargitay.gov.tr/YargitayBilgiBankasiIstemciWeb/"

   driver1 = Driver(url1)

   action = ActionChains(driver1.driver, 1000)

   captcha.save_current_img(driver1)

   driver1.get_detayli_arama_we().location_once_scrolled_into_view
   time.sleep(1)
   driver1.get_detayli_arama_we().click()
   time.sleep(1)


   driver1.get_captcha_input_we().location_once_scrolled_into_view
   time.sleep(1)
   action.send_keys_to_element(driver1.get_captcha_input_we(), captcha.get_captcha_code())
   action.perform()


   driver1.get_karar_yili_we().location_once_scrolled_into_view
   time.sleep(1)
   driver1.get_karar_yili_we().send_keys(str(start_date.year))


   driver1.get_tarih_bas_we().location_once_scrolled_into_view
   time.sleep(1)
   driver1.get_tarih_bas_we().send_keys(get_str_date(start_date))
   

   driver1.get_tarih_son_we().location_once_scrolled_into_view
   time.sleep(1)
   driver1.get_tarih_son_we().send_keys(get_str_date(end_date))

   driver1.get_search_we().location_once_scrolled_into_view
   driver1.get_search_we().send_keys(Keys.RETURN)

   time.sleep(3)


   print("1\n")

 

   count_element = driver1.driver.execute_script("return document.getElementById(\"aramaForm:sonucTable_data\").childElementCount")
   
   
   print("1.5\n")
   
   driver1.data_ri_click(0)
   print("2\n")