import logging
from selenium.webdriver.common.keys import Keys
import captcha
import time
from selenium.webdriver.common.action_chains import ActionChains
from my_tools import get_str_date

import pandas as pd
from Karar import Karar

from MSSQL import MSSQL


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


   count_element = driver1.driver.execute_script("return document.getElementById(\"aramaForm:sonucTable_data\").childElementCount")
   

   for i in range(0, count_element):

      
      try:
         driver1.data_ri_click(i)
      except:
         logging.error(str(i) + ". satıra tıklanamadı!")
      else:
         time.sleep(1)
         try:
            icerik = driver1.copy_karar_icerik_panel()
         except BaseException as err:
            logging.error("data_ri_click("+str(i)+") tıklama başarılı ancak kopyalama başarısız\n" + err)
         else:

            print(icerik.get_attribute("innerHTML") + "\nBİTTİ\n\n")

            daire
            tarih
            kararYil
            kararNo
            esasYil
            esasNo
            mahkemesi
            metin = icerik.get_attribute("innerHTML")

            karar = Karar("w", "11/11/2021", 2021, 123, 2022, 124, "nn", metin)
            mssql = MSSQL()
      
      if i == 0:
         break
         


   print("2\n")