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

   captcha.save_current_img(driver1.driver)


   #action.perform()
   action.move_to_element(driver1.get_captcha_input_we())
   action.send_keys_to_element(driver1.get_captcha_input_we(), captcha.get_captcha_code())
   action.perform()

   # action.move_to_element(driver1.get_karar_yili_we())
   # action.send_keys_to_element(driver1.get_karar_yili_we(), str(start_date.year))
   # action.perform()
   driver1.get_karar_yili_we().send_keys(str(start_date.year))


   # action.move_to_element(driver1.get_tarih_bas_we())
   # action.send_keys_to_element(driver1.get_tarih_bas_we(),  get_str_date(start_date) )
   # action.perform()
   driver1.get_tarih_bas_we().send_keys(get_str_date(start_date))
   
   #action.move_to_element(driver1.get_tarih_son_we())
   # action.send_keys_to_element(driver1.get_tarih_son_we(), get_str_date(end_date) )
   # action.perform()
   driver1.get_tarih_son_we().send_keys(get_str_date(end_date))

   action.move_to_element_with_offset(driver1.get_search_we(),0, 0)
   action.perform()
   driver1.get_search_we().send_keys(Keys.RETURN)
   
