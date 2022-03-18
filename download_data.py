from asyncio.windows_events import NULL
from lib2to3.pgen2 import driver
import logging
from numpy import compare_chararrays
from selenium.webdriver.common.keys import Keys
import captcha
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from captcha_read import captcha_read
from my_tools import control_panel, get_mahkemesi, get_no, get_str_date, get_yil, hata

import pandas as pd
from Karar import Karar

from MSSQL import MSSQL


from Driver import Driver



def download_data(year, restartCount, start_esasNo=-1, end_kararNo=-1, ):


   url1= "https://karararama.yargitay.gov.tr/YargitayBilgiBankasiIstemciWeb/"

   mssql = MSSQL(restartCount)

   driver1 = Driver(url1, restartCount)



   while(True):


      if( mssql.conn.isActive  == False):

         mssql.mssql_close()
         
         mssql_connection_status = mssql.mssql_connect()

         if( mssql_connection_status == "quit" ):
            return "quit"

         elif( mssql_connection_status == "restart"):

            return "restart"

         else:
            pass


      if(driver1.isActive == False):

         driver1.driver_close()

         driver_connection_status = driver1.connect_driver()

         if( driver_connection_status == "quit" ):
            return "quit"

         elif(driver_connection_status == True):
            pass

         elif(driver_connection_status == "restart"):
            return "restart"


      last_karar = mssql.last_karar(year)

      if(last_karar == "quit"):
         return "quit"

      elif(last_karar == "restart"):
         return "restart"

      else:      #diğer durumlarda geçerli bir last_karar numarası gelmiştir
         pass


      action = ActionChains(driver1.driver, 250)

      is_img_refresh = captcha.did_img_refresh()

      if(is_img_refresh == "restart"):
         return "restart"
      elif(is_img_refresh == "quit"):
         return "quit"

      error_count = 0

      try: # 1. try except

         if( is_img_refresh == True ):

            captcha.save_current_img(driver1)

         driver1.get_detayli_arama_we().location_once_scrolled_into_view
         time.sleep(0.1)

         driver1.get_detayli_arama_we().click()
         time.sleep(0.1)


         driver1.get_captcha_input_we().location_once_scrolled_into_view
         time.sleep(0.1)

         captcha_code = captcha_read()

         if( captcha_code == "quit"):
            return "quit"

         elif(captcha_code == "restart"):
            return "res"
         
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


         

      except BaseException as err:

         if(restartCount[0] == 1 and error_count == 5):

            logging.error("1. try except hata!: " + str(err))
            
            x = control_panel()

            x = control_panel(str(err))

            if(x == "resume"):

               error_count = 0
               continue
            
            elif(x == "restart"):
               return "restart"
            
            elif(x == "quit"):
               return "quit"

         error_count += 1

         if(error_count == 5):
            return "restart"

         logging.error("download_data() 1. try except hata!: " + str(err))

         continue


      try:
         result_sonucTable = driver1.is_there_sonucTable_head()

      except BaseException as err:

         logging.warning( "\nis_there_sonucTable_head() hata!:{}".format(err) )

         message = driver1.is_there_message()

         if(message == NULL):

            logging.error("is_there_sonucTable_head() fonksiyonu içerisinde is_there_message() fonksiyonundan geriye mesaj web elementinin olmadığı hatası alındı.")

            if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):
                  continue
               
               elif(x == "restart"):
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"

            return "restart"
            
         elif(message == "message could not be read"):

            logging.error( "(2. try except) mesaj kutusu var ancak mesaj okunamadı, hata!" + str(err)  )

            if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):

                  continue
               
               elif(x == "restart"):
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"

            return "restart"


      try:

         count_element = driver1.driver.execute_script("return document.getElementById(\"aramaForm:sonucTable_data\").childElementCount")

      except:

         logging.error("(3. try except) aramaForm:sonucTable_data sonucunda kaç adet satır olduğu alınamadı")

         if( restartCount[0] == 1):

               x = control_panel(str(err))

               if(x == "resume"):

                  continue
               
               elif(x == "restart"):
                  return "restart"
               
               elif(x == "quit"):
                  return "quit"

         return "restart"
      

      for i in range(0, count_element):


         data_ri = driver1.get_data_ri_we(i).find_elements(By.CSS_SELECTOR, "td[role='gridcell']")

         sira     = data_ri[0].text
         daire    = data_ri[1].text

         esas     = data_ri[2].text
         esasNo   = get_no(esas)
         esasYil  = get_yil(esas)
         
         karar    = data_ri[3].text
         kararNo  = get_no(karar)
         kararYil = get_yil(karar)
         k_tarih  = data_ri[4].text

         
         
         data_ri_click_result = driver1.data_ri_click(i)
         
         if(data_ri_click_result == False):

            logging.error(str(i) + ". satıra tıklanamadı!")

            if( restartCount[0] == 1):

               while (True):

                  x = control_panel( str(err) )

                  if(x == "resume"):
                     "Print for döngüsü içersinde resume seçeneği seçilemez!!"
                     continue
                  
                  elif(x == "restart"):
                     return "restart"
                  
                  elif(x == "quit"):
                     return "quit"

            return "restart"

         
         
         try:
            icerik = driver1.copy_karar_icerik_panel()
         except BaseException as err:

            logging.error("data_ri_click("+str(i)+") tıklama başarılı ancak kopyalama başarısız\n" + err)

            if( restartCount[0] == 1):

               while (True):

                  x = control_panel( str(err) )

                  if(x == "resume"):
                     "Print for döngüsü içersinde resume seçeneği seçilemez!!"
                     continue
                  
                  elif(x == "restart"):
                     return "restart"
                  
                  elif(x == "quit"):
                     return "quit"

            return "restart"

         else:

            metin = icerik.get_attribute("innerHTML")

            mahkemesi = get_mahkemesi(metin)
            
            karar = Karar(daire, k_tarih, kararYil, kararNo, esasYil, esasNo, mahkemesi, metin)

            karar.karar_print(False)

            save_status = mssql.save(karar)

            if(save_status == False):

               if( restartCount[0] == 1):

                  while (True):

                     x = control_panel( str(err) )

                     if(x == "resume"):
                        "Print for döngüsü içersinde resume seçeneği seçilemez!!"
                        continue
                     
                     elif(x == "restart"):
                        return "restart"
                     
                     elif(x == "quit"):
                        return "quit"

               return "restart"



            restartCount[0] = 0  #Eğer bir restart sonrası bir belge başarı
                                 #ile kaydedilebilirse restartCount sıfırlandı
         
         if i == 3:
            break
